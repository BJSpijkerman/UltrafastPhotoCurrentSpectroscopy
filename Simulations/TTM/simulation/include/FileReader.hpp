#include <vector>
#include <string>

#ifndef FILE_READER_HPP
#define FILE_READER_HPP

struct FileData
{
	std::vector<double> x;
	std::vector<double> y;
};

FileData readFile(const std::string& f_path);

#endif
