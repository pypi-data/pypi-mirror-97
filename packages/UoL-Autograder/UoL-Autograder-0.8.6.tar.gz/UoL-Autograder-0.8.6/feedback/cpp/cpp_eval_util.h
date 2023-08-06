#ifndef _CPP_EVAL_UTIL_H
#define _CPP_EVAL_UTIL_H

#include "json.hpp"
#include <vector>
#include <string>
#include <fstream>
#include <tuple>
#include <iostream>
#include <cstdlib>
#include <stdlib.h>
#include <cstdlib>


using namespace std;
using namespace nlohmann;



tuple<string, float> process_result(vector<string> result, vector<string> test_case, string question_specific_fail_message = "");
bool is_within_margin(float a, float b, float margin);
bool is_within_margin(double a, double b, double margin);
string byte_to_binary(int x);
string vector_to_string(vector<int> a);
string vector_to_string(vector<float> a);
string vector_to_string(vector<double> a);
string vector_to_string(vector<string> a);


// SHA256 source from: http://www.zedwood.com/article/cpp-sha256-function

/*
 * Updated to C++, zedwood.com 2012
 * Based on Olivier Gay's version
 * See Modified BSD License below: 
 *
 * FIPS 180-2 SHA-224/256/384/512 implementation
 * Issue date:  04/30/2005
 * http://www.ouah.org/ogay/sha2/
 *
 * Copyright (C) 2005, 2007 Olivier Gay <olivier.gay@a3.epfl.ch>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the project nor the names of its contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE PROJECT AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE PROJECT OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */
class SHA256
{
protected:
    typedef unsigned char uint8;
    typedef unsigned int uint32;
    typedef unsigned long long uint64;
 
    const static uint32 sha256_k[];
    static const unsigned int SHA224_256_BLOCK_SIZE = (512/8);
public:
    void init();
    void update(const unsigned char *message, unsigned int len);
    void final(unsigned char *digest);
    static const unsigned int DIGEST_SIZE = ( 256 / 8);
 
protected:
    void transform(const unsigned char *message, unsigned int block_nb);
    unsigned int m_tot_len;
    unsigned int m_len;
    unsigned char m_block[2*SHA224_256_BLOCK_SIZE];
    uint32 m_h[8];
};
 
std::string sha256(std::string input);
 
#define SHA2_SHFR(x, n)    (x >> n)
#define SHA2_ROTR(x, n)   ((x >> n) | (x << ((sizeof(x) << 3) - n)))
#define SHA2_ROTL(x, n)   ((x << n) | (x >> ((sizeof(x) << 3) - n)))
#define SHA2_CH(x, y, z)  ((x & y) ^ (~x & z))
#define SHA2_MAJ(x, y, z) ((x & y) ^ (x & z) ^ (y & z))
#define SHA256_F1(x) (SHA2_ROTR(x,  2) ^ SHA2_ROTR(x, 13) ^ SHA2_ROTR(x, 22))
#define SHA256_F2(x) (SHA2_ROTR(x,  6) ^ SHA2_ROTR(x, 11) ^ SHA2_ROTR(x, 25))
#define SHA256_F3(x) (SHA2_ROTR(x,  7) ^ SHA2_ROTR(x, 18) ^ SHA2_SHFR(x,  3))
#define SHA256_F4(x) (SHA2_ROTR(x, 17) ^ SHA2_ROTR(x, 19) ^ SHA2_SHFR(x, 10))
#define SHA2_UNPACK32(x, str)                 \
{                                             \
    *((str) + 3) = (uint8) ((x)      );       \
    *((str) + 2) = (uint8) ((x) >>  8);       \
    *((str) + 1) = (uint8) ((x) >> 16);       \
    *((str) + 0) = (uint8) ((x) >> 24);       \
}
#define SHA2_PACK32(str, x)                   \
{                                             \
    *(x) =   ((uint32) *((str) + 3)      )    \
           | ((uint32) *((str) + 2) <<  8)    \
           | ((uint32) *((str) + 1) << 16)    \
           | ((uint32) *((str) + 0) << 24);   \
}

class Results
{
public:
   void add(std::string question, std::string score, float weight, std::string feedback);
   void set(int i, std::string question, std::string score, float weight, std::string feedback);
   void output(const char* filename);
   void output(char* filename);
   void output(const char* filename, const char* validator_filename, string secret);

private:
   std::vector<nlohmann::json> _test_results;
};

template<class T>
class Evaluator
{
  public:
    Evaluator(int argc, char** argv) : 
      _skip(argc >= 3 ? atoi(argv[2]) : 0)
    {
      _output_file = argc >= 2 ? argv[1] : "";
      _secret_location = argc >= 4 ? argv[3] : "";
      _secret_key = GetSecret(_secret_location);
    }

    virtual string GetName(int i) = 0;
    virtual T GetResult(int i) = 0;
    virtual float GetScore(int i, T result) = 0;
    virtual string GetFeedback(int i, T result, float score) = 0;

    int Run(){
      if(_output_file.empty()) { return 1; }
      
      std::string name;
      int n = -1;
      do{
        name = GetName(++n);
      } while(!name.empty());

      for(int i = 0; i < n; i++){
         _results.add(GetName(i), "", 1.0/n, "");
      }
      WriteResults();

      string feedback = "";
      for(int i = _skip; i < n; i++){
        printf("%d\n", i);
        float score = 0;
        try{
          T result = GetResult(i);
          score = GetScore(i, result);
          feedback = GetFeedback(i, result, score);
        }
        catch (exception& e)
        {
          feedback = "An error occured:\n";
          feedback += e.what();
          feedback += "\n : FAIL!";
        }
        _results.set(
           i,
          GetName(i),
          to_string(score),
          1.0/n,
          feedback);
         WriteResults();
      }
      WriteResults();
      return 0;
    }

  private:
    int _skip;
    Results _results;
    std::string _secret_key;
    std::string _secret_location;
    std::string _output_file;

    string GetSecret(string secret_location)
    {
      if(secret_location.empty()){
        return secret_location;
      }
      std::string secret_key(getenv(secret_location.c_str()));
#ifndef _WIN32 
      unsetenv(secret_location.c_str());
#endif
      return secret_key;
    }

    void WriteResults(){
      if(_secret_key.empty()){
        _results.output(_output_file.c_str());
      }
      else{
        _results.output(_output_file.c_str(), _secret_location.c_str(), _secret_key);
      }
    }
};

#endif