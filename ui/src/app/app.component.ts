import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { Observable, of } from 'rxjs';

interface Currency {
  name: string;
  code: string;
}
interface CoinValue {
  date: string,
  price: string
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'CryptoTracker';
  BASE_URL = "http://localhost/api/";
  baseCurrencyMenu: Currency[] = null;
  secondCurrencyMenu: Currency[] = null;
  selectedBaseCurrency: any;
  selectedSecondCurrency: any;
  isChartDataSuccess: boolean = false;
  coinHistoryData: CoinValue[] = null;
  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.setupBaseCurrencyDropdown();
  }

  setupBaseCurrencyDropdown = (): void => {
    const currencies_endpoint = `currencies`;
    this.http.get<any>(this.BASE_URL + currencies_endpoint).subscribe(data => {
      this.baseCurrencyMenu = data["res"];
      this.selectedBaseCurrency = data["res"][0]["code"];
      this.setupSecondCurrencyDropdown();
    })
  }

  setupSecondCurrencyDropdown = (): void => {
    const currencies_endpoint = `currencies?selected=${this.selectedBaseCurrency}`;
    this.http.get<any>(this.BASE_URL + currencies_endpoint).subscribe(data => {
      this.secondCurrencyMenu = data["res"];
      this.selectedSecondCurrency = data["res"][1]["code"];
    })
  }

  fetchCoinData = (): void => {
    const period = "7";
    const round_results_endpoint = `coin_history?base=${this.selectedBaseCurrency}&second_currency=${this.selectedSecondCurrency}&period=${period}`;
    this.http.get<any>(this.BASE_URL + round_results_endpoint).subscribe(data => {
      this.isChartDataSuccess = true;
      this.coinHistoryData = data;
    })
  }

  selectBaseCurrency = (event: Event): void => {
    this.selectedBaseCurrency = (event.target as HTMLSelectElement).value;
    this.setupSecondCurrencyDropdown();
  }

	selectSecondCurrency = (event: Event): void => {
    this.selectedSecondCurrency = (event.target as HTMLSelectElement).value;
    this.fetchCoinData();
	}

}
