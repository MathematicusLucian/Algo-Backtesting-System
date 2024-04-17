export interface Currency {
    name: string;
    code: string;
}
export interface CoinValue {
    date: string,
    price: string
}

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment as env } from '../../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class CurrencyDataService {
  private apiUrl = env.apiUrl;

  constructor(private http: HttpClient) {}

  setupBaseCurrencyDropdown = (): any => {
    const currencies_endpoint = `/currencies`;
    return this.http.get<any>(this.apiUrl + currencies_endpoint);
  }

  setupSecondCurrencyDropdown = (selectedBaseCurrency: any): any => {
    const currencies_endpoint = `/currencies?selected=${selectedBaseCurrency}`;
    return this.http.get<any>(this.apiUrl + currencies_endpoint);
  }

  fetchCoinData = (selectedBaseCurrency: any, selectedSecondCurrency: any, period: any): any => {
    const round_results_endpoint = `/coin_history?base=${selectedBaseCurrency}&second_currency=${selectedSecondCurrency}&period=${period}`;
    return this.http.get<any>(this.apiUrl + round_results_endpoint);
  }

}