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

  setupBaseCurrencyDropdown(): void {
    const currencies_endpoint = `currencies`;
    this.http.get<any>(this.BASE_URL + currencies_endpoint).subscribe(data => {
      this.baseCurrencyMenu = data["res"];
      this.selectedBaseCurrency = data["res"][0];
      console.log("selectedBaseCurrency",this.selectedBaseCurrency);
      this.setupSecondCurrencyDropdown();
    })
  }

  setupSecondCurrencyDropdown(): void {
    const currencies_endpoint = `currencies?selected=${this.selectedBaseCurrency.code}`;
    this.http.get<any>(this.BASE_URL + currencies_endpoint).subscribe(data => {
      this.secondCurrencyMenu = data["res"];
    })
  }

  fetchCoinData(): void {
    const round_results_endpoint = `round_results?base=${this.selectedBaseCurrency.code}&second_currency=${this.selectedSecondCurrency.code}`;
    this.http.get<any>(this.BASE_URL + round_results_endpoint).subscribe(data => {
      this.isChartDataSuccess = true;
      this.coinHistoryData = data;
    })
  }

  selectBaseCurrency(event: Event): void {
    this.selectedBaseCurrency = (event.target as HTMLSelectElement).value;
    this.setupSecondCurrencyDropdown();
  }

	selectSecondCurrency(event: Event): void {
    this.selectedSecondCurrency = (event.target as HTMLSelectElement).value;
    this.fetchCoinData();
	}

}
