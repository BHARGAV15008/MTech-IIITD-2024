#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iomanip>
#include "q1.cpp"
using namespace std;
int noOfEntry = 0; // initially count is 0

struct PriceInflation
{
    int year;
    float gPrices;
    float inf;
};

class LongtermCapitalGainsTax
{
    PriceInflation *infData;
    long bPrice;
    int sYear;
    int bYear;

public:
    LongtermCapitalGainsTax(string &filepath, int sYear)
    {
        this->infData = loadData(filepath);
        this->bPrice = 5000000;
        this->sYear = sYear;
        this->bYear = 2010;
    }

    PriceInflation *loadData(string &filepath)
    {
        ifstream infCsv(filepath);
        string entry;
        PriceInflation records;
        while (getline(infCsv, entry))
            if (!entry.empty())
                noOfEntry++;

        PriceInflation *datas = new PriceInflation[noOfEntry - 1];
        infCsv.clear();
        infCsv.seekg(0);
        getline(infCsv, entry);

        int idx = 0;
        while (getline(infCsv, entry))
        {
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

    float calcSellingPrice()
    {
        double eSellPrice = this->bPrice;
        // // Approach 1:
        // for (int i = 0; i < noOfEntry; i++) {
        //     if (this->sYear < 2024){
        //         if (infData[i].year > this->bYear && infData[i].year <= this->sYear)
        //             eSellPrice *= (1 + (infData[i].gPrices - infData[i].inf) / 100);
        //     }
        //     else {
        //         if (infData[i].year > this->bYear && infData[i].year <= this->sYear)
        //             eSellPrice *= (1 + (infData[i].gPrices) / 100);
        //     }
        // }

        // Approach 2:
        for (int i = 0; i < noOfEntry; i++)
        {
            if (infData[i].year > this->bYear && infData[i].year <= this->sYear)
            {
                if (infData[i].year < 2024)
                    eSellPrice *= (1 + (infData[i].gPrices - infData[i].inf) / 100);
                else
                    eSellPrice *= (1 + (infData[i].gPrices) / 100);
            }
        }
        return eSellPrice;
    }

    float calcProfit()
    {
        double sPrice = this->calcSellingPrice();
        return sPrice - this->bPrice;
    }

    float calcLTG()
    {
        double profit = this->calcProfit();
        return this->sYear < 2024 ? (profit <= 0 ? 0 : 0.2 * profit) : (profit <= 0 ? 0 : 0.125 * profit);
    }
};

int main()
{
    long bPrice, bYear, sYear;
    string filepath = "price-inflation.csv";
    cout << "Enter your Selling year (2010 - 2030): ";
    cin >> sYear;

    LongtermCapitalGainsTax1 ltcg1 = LongtermCapitalGainsTax1(filepath, sYear);
    LongtermCapitalGainsTax ltcg = LongtermCapitalGainsTax(filepath, sYear);
    cout << "Question 1: Evaluation " << endl;
    cout << "Q1: Selling Price at " << fixed << setprecision(2) << sYear << " is " << ltcg1.calcSellingPrice() << endl;
    cout << "Q1: LTCG Tax at " << fixed << setprecision(2) << sYear << " is " << ltcg1.calcLTG() << endl;
    cout << endl;
    cout << "Question 2: Evaluation " << endl;
    cout << "Q2: Selling Price at " << fixed << setprecision(2) << sYear << " is " << ltcg.calcSellingPrice() << endl;
    cout << "Q2: LTCG Tax at " << fixed << setprecision(2) << sYear << " is " << ltcg.calcLTG() << endl;
    cout << endl;
    cout << "Comparison between First and Second Scheme." << endl;
    cout << "Difference (Scheme After 2024 - Scheme Before 2024): " << ltcg.calcLTG() - ltcg1.calcLTG() << endl;

    return 0;
}