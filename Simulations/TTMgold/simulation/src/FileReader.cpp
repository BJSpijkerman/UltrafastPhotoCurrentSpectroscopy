#include "FileReader.hpp"
#include <fstream>
#include <iostream>
#include <stdexcept>


FileData readFile(const std::string& f_path)
{
	FileData data;
	std::ifstream file(f_path);
	if (!file.is_open())
	{
		throw std::runtime_error("Error in opening file: " + f_path);
	}

	double val_x, val_y;
	while (file >> val_x >> val_y)
	{
		data.x.push_back(val_x);
		data.y.push_back(val_y);
	}

	std::cout << "Successfully processed " << data.x.size() << " data pairs from " << f_path << std::endl;
	return data;
}
