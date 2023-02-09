/**
 * @file WIBtoWIB2.hpp Implementation of functions to convert files from the old WIB format to WIB2
 *
 * This is part of the DUNE DAQ , copyright 2020.
 * Licensing/copyright details are in the COPYING file that you should have
 * received with this code.
 */

#ifndef RAWDATAUTILS_INCLUDE_WIBTOWIB2_HPP_
#define RAWDATAUTILS_INCLUDE_WIBTOWIB2_HPP_

#include <cstdint>
#include <iostream>
#include <fstream>
#include <filesystem>
#include "detdataformats/wib/WIBFrame.hpp"
#include "detdataformats/wib2/WIB2Frame.hpp"

namespace dunedaq {
namespace rawdatautils {

detdataformats::wib2::WIB2Frame
wibtowib2(detdataformats::wib::WIBFrame* fr, uint64_t timestamp=0) {
  detdataformats::wib2::WIB2Frame res;
  for (int i = 0; i < 256; ++i) {
    res.set_adc(i, fr->get_channel(i));
  }
  auto header = fr->get_wib_header();
  res.header.version = header->version;
  res.header.crate = header->crate_no;
  res.header.slot = header->slot_no;
  res.header.link = header->fiber_no;
  res.set_timestamp(timestamp);
  return res;
}

void
wib_binary_to_wib2_binary(std::string& filename, std::string& output) {
  std::ifstream file(filename.c_str(), std::ios::binary);
  std::ofstream out(output.c_str(), std::ios::binary);
  std::cout << "Transforming " << filename << " to " << output << '\n';
  auto size = std::filesystem::file_size(filename);
  std::vector<char> v(size);
  file.read(v.data(), size);
  file.close();
  int num_frames = size / sizeof(detdataformats::wib::WIBFrame);
  std::cout << "Number of frames found: "<< num_frames << '\n';
  auto ptr = reinterpret_cast<detdataformats::wib::WIBFrame*>(v.data());
  uint64_t timestamp = ptr->get_timestamp();
  uint64_t first_timestamp = timestamp;
  int count = 0;
  while(num_frames--){
    auto new_ts = ptr->get_timestamp();
    if ((new_ts - first_timestamp) != count++ * 25) {
      std::cout << "Timestamp " << new_ts << " doesn't differ by 25 from the previous timestamp";
      std::cout << ", it will be overwritten " << '\n';
    }
    auto wib2fr = wibtowib2(ptr, timestamp);
    timestamp += 32;
    ptr++;
    out.write(reinterpret_cast<char*>(&wib2fr), sizeof(wib2fr));
  }
  out.close();
}

void
wib_hdf5_to_wib2_binary(std::string& filename, std::string& output) {
}


} // namespace dunedaq::rawdatautils
}

#endif // RAWDATAUTILS_INCLUDE_WIBTOWIB2_HPP_
