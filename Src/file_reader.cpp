#include <fstream>
#include <iostream>
std::ifstream  fin;
int t;
void readfile()
{
//  fin.open("input_matrix.dat");

  int read_time, i, j;
  //while (fin >> i && fin >>j)
  int count = 3;
  auto read_location = fin.tellg() ;

  //std::cout << "t = " << t << '\n';
  //std::cout << "read = " << read_time << '\n';
  for (size_t k = 0 ;  ; k++)
  {
    read_location = fin.tellg() ;
    fin >> read_time;
    if (read_time != t)
     break;
    //std::cout << "Enter!" << '\n' << '\n';
    fin >> i ; fin >>j ;

    std::cout << "t: " << t << '\n';
    std::cout << i << '-';
    std::cout << j << '\n' << '\n';

    //fin>>text;
  }
  fin.clear();
  fin.seekg(read_location, fin.beg);
}
void restart_read_file()
{
  std::cout << "rest!" << '\n';
  fin.clear();
  fin.seekg(0, fin.beg);
  fin.close();
  fin.open("input_matrix.dat");
  if (!fin)
  {
    std::cerr << "Unable to open file datafile.txt";
    exit(1);   // call system to stop
  }

}

int main()
{
  int count = 30100;
  restart_read_file();

  for (t = 28600; t < count; t+=20)
  {
    readfile();

  }

}
