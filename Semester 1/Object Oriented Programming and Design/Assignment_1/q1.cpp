#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip>
using namespace std;
int noOfEntry1 = 0; // initially count is 0

struct PriceInflation1 {
    int year;
    float gPrices;
    float inf;
};

class LongtermCapitalGainsTax1 {
    PriceInflation1* infData;
    long bPrice;
    int sYear;
    int bYear;

    public:
        LongtermCapitalGainsTax1(string &filepath, int sYear) {
            this->infData = loadData(filepath);
            this->bPrice = 5000000;
            this->sYear = sYear;
            this->bYear = 2010;
        }

        PriceInflation1* loadData(string &filepath) {
            ifstream infCsv(filepath);
            string entry;
            PriceInflation1 records;
            while (getline(infCsv, entry))
                if (!entry.empty()) noOfEntry1++;

            PriceInflation1* datas = new PriceInflation1[noOfEntry1 - 1];
            infCsv.clear();
            infCsv.seekg(0);
            getline(infCsv, entry);

            int idx = 0;
            while (getline(infCsv, entry)) {
                stringstream ss(entry);
                string dt;
                string oItem;

                getline(ss, dt, ',');
                records.year = stoi(dt.substr(0, 4));

                getline(ss, oItem, ',');
                records.gPrices = stod(oItem);

                getline(ss, oItem, ',');
                records.inf = stod(oItem);

                datas[idx++] = records;
            }
            return datas;
        }

        float calcSellingPrice() {
            double eSellPrice = this->bPrice;
            for (int i = 0; i < noOfEntry1; i++)
                if (infData[i].year > this->bYear && infData[i].year <= this->sYear)
                    eSellPrice *= (1 + (infData[i].gPrices - infData[i].inf) / 100);
                    
            return eSellPrice;
        }

        float calcProfit() {
            double sPrice = this->calcSellingPrice();
            return sPrice - this->bPrice;
        }

        float calcLTG() {
            double profit = this->calcProfit();
            return profit <= 0 ? 0 : 0.2 * profit;
        }
};

