#include <iostream>
#include <filesystem>

int main() {
    try {
        // Attempt to traverse up one directory and list contents (read-only)
        std::filesystem::path current = std::filesystem::current_path();
        std::filesystem::path parent = current.parent_path();
        
        std::cout << "Current directory: " << current << std::endl;
        std::cout << "Parent directory: " << parent << std::endl;
        
        // Try to list parent directory contents (without deletion)
        for (const auto& entry : std::filesystem::directory_iterator(parent)) {
            std::cout << "Found: " << entry.path().filename() << std::endl;
        }
    } catch (const std::exception& e) {
        std::cout << "Access denied or error: " << e.what() << std::endl;
    }
    return 0;
}