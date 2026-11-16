import numpy as np
import ufl
from dolfinx import mesh, fem, io
from dolfinx.fem import petsc           # <-- Add this line
from dolfinx.io import gmsh
from mpi4py import MPI
from petsc4py import PETSc
# ==============================================================================
# 1. LOAD MESH & CONVERT UNITS
# ==============================================================================
domain, cell_tags, facet_tags, *_ = gmsh.read_from_msh(
    "mesh/beam.msh", 
    MPI.COMM_WORLD, 
    rank=0, 
    gdim=3
)

# Convert mesh coordinates from mm to meters
domain.geometry.x[:] *= 1e-3

x_min, x_max = np.min(domain.geometry.x[:, 0]), np.max(domain.geometry.x[:, 0])
y_min, y_max = np.min(domain.geometry.x[:, 1]), np.max(domain.geometry.x[:, 1])
z_min, z_max = np.min(domain.geometry.x[:, 2]), np.max(domain.geometry.x[:, 2])

print(f"Domain X bounds (m): [{x_min:.4f}, {x_max:.4f}]")
print(f"Domain Y bounds (m): [{y_min:.4f}, {y_max:.4f}]")
print(f"Domain Z bounds (m): [{z_min:.4f}, {z_max:.4f}]")

V = fem.functionspace(domain, ("Lagrange", 1, (3,)))

# ==============================================================================
# 2. MATERIAL PROPERTIES & PHYSICAL PARAMETERS (SI Units)
# ==============================================================================
E = 210E9          # Pa
nu = 0.3           # Poisson ratio
rho = 7850.0       # kg/m^3
g_acc = 9.81       # m/s^2

lambda_ = E * nu / ((1.0 + nu) * (1.0 - 2.0 * nu))
mu = E / (2.0 * (1.0 + nu))

# ==============================================================================
# 3. BOUNDARY CONDITIONS (Fixed Support Feet = Tag 1)
# ==============================================================================
facet_dim = domain.topology.dim - 1
feet_facets = facet_tags.find(1)
feet_dofs = fem.locate_dofs_topological(V, facet_dim, feet_facets)

u_fixed = np.zeros(3, dtype=PETSc.ScalarType)
bc = fem.dirichletbc(u_fixed, feet_dofs, V)

# ==============================================================================
# 4. MEASURES & MOVABLE RECTANGULAR UNIFORM SURFACE LOAD SETUP
# ==============================================================================
dx = ufl.Measure("dx", domain=domain, subdomain_data=cell_tags)
ds = ufl.Measure("ds", domain=domain, subdomain_data=facet_tags)

# Volumetric Self-Weight
f_gravity = fem.Constant(domain, np.array([0.0, 0.0, -rho * g_acc], dtype=PETSc.ScalarType))

# Load parameters
patch_center_y = (y_max + y_min) / 2.0  
patch_length = 48.3e-3                  # 48.3 mm in meters
patch_width = 45.0e-3                   # 45.0 mm in meters
q_pressure = 1e7                        # 10 MPa load for visible displacement

class MovableRectangularLoad:
    def __init__(self, center, length, width, q_uniform, z_top):
        self.x_c, self.y_c = center
        self.half_l = length / 2.0
        self.half_w = width / 2.0
        self.q_uniform = q_uniform
        self.z_top = z_top

    def __call__(self, x):
        values = np.zeros((3, x.shape[1]), dtype=PETSc.ScalarType)
 
        in_x = (x[0] >= (self.x_c - self.half_l)) & (x[0] <= (self.x_c + self.half_l))
        in_y = (x[1] >= (self.y_c - self.half_w)) & (x[1] <= (self.y_c + self.half_w))
        
        # Relaxed Z tolerance (atol=1e-3 m = 1 mm) to reliably catch top surface nodes
        on_z = np.isclose(x[2], self.z_top, atol=1e-3)

        inside_patch = in_x & in_y & on_z
        values[2, inside_patch] = -self.q_uniform
        
        return values

T_surface = fem.Function(V)

# ==============================================================================
# 5. VARIATIONAL FORMULATION
# ==============================================================================
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)

def epsilon(u):
    return ufl.sym(ufl.grad(u))

def sigma(u):
    return lambda_ * ufl.tr(epsilon(u)) * ufl.Identity(3) + 2.0 * mu * epsilon(u)

a = ufl.inner(sigma(u), epsilon(v)) * dx
L_form = ufl.inner(f_gravity, v) * dx + ufl.inner(T_surface, v) * ds(2)

# ==============================================================================
# 6. EXPLICIT SOLVER SETUP (DOLFINx v0.10+ Compliant)
# ==============================================================================
a_comp = fem.form(a)
L_comp = fem.form(L_form)

# Assemble Matrix A outside the loop using the explicit petsc import
A = petsc.assemble_matrix(a_comp, bcs=[bc])
A.assemble()

solver = PETSc.KSP().create(domain.comm)
solver.setOperators(A)
solver.setType("preonly")
solver.getPC().setType("lu")
solver.getPC().setFactorSolverType("mumps")

# Extract function spaces for create_vector (Required in modern DOLFINx)
b = petsc.create_vector(fem.extract_function_spaces(L_comp))
uh = fem.Function(V)
uh.name = "Displacement"

# ==============================================================================
# 7. TIME-STEPPING (LOAD SHIFTING) & EXPORT
# ==============================================================================
num_steps = 20
x_start = x_min + patch_length / 2.0
x_end = x_max - patch_length / 2.0
x_positions = np.linspace(x_start, x_end, num_steps)
time_steps = np.linspace(0.0, 1.0, num_steps)

with io.XDMFFile(domain.comm, "out/beam_displacement_transient.xdmf", "w") as xdmf:
    xdmf.write_mesh(domain)
    
    for step, (t, x_pos) in enumerate(zip(time_steps, x_positions)):
        print(f"\n--- Step {step+1}/{num_steps} : t = {t:.2f} ---")
        
        # 1. Reset the load field to absolute zero
        T_surface.x.array[:] = 0.0
        
        # 2. Shift load position
        T_surface.interpolate(MovableRectangularLoad(
            center=(x_pos, patch_center_y),
            length=patch_length,
            width=patch_width,
            q_uniform=q_pressure,
            z_top=z_max
        ))
        
        # 3. Reassemble the RHS vector
        with b.localForm() as b_loc:
            b_loc.set(0.0)
            
        petsc.assemble_vector(b, L_comp)
        petsc.apply_lifting(b, [a_comp], bcs=[[bc]])
        b.ghostUpdate(addv=PETSc.InsertMode.ADD_VALUES, mode=PETSc.ScatterMode.REVERSE)
        petsc.set_bc(b, [bc])
        
# 4. Solve the system
        solver.solve(b, uh.x.petsc_vec)
        uh.x.scatter_forward()
        
        disp_norms = np.linalg.norm(uh.x.array.reshape(-1, 3), axis=1)
        print(f"Max displacement: {np.max(disp_norms)*1e3:.4f} mm")
        
        # 5. Append step to file
        xdmf.write_function(uh, t)

print("\nAnimation successfully saved.")
