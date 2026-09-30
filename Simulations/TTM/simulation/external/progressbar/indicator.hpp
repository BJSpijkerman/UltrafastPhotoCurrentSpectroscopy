#ifndef INDICATOR_HPP
#define INDICATOR_HPP

#include <ostream>

class IIndicator {
public:
    virtual ~IIndicator() = default;

    // Render exactly ONE line (no newline)
    virtual void write_progress(std::ostream& os) = 0;


};

#endif
