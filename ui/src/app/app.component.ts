import { Component, OnInit, AfterViewInit, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { environment as env } from '../environments/environment';
import * as LightweightCharts from 'lightweight-charts';
import { Subject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import { IonicModule } from '@ionic/angular';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect } from '@angular/material/select';
import { HeaderComponent } from './components/header/header.component';
import { MatInput } from '@angular/material/input';
import { MatSidenavContainer, MatSidenavContent } from '@angular/material/sidenav';
import { Sidenav } from './components/sidenav/sidenav.component';
import { ChartDataService } from './services/chart-data/chart-data.service';
import { CurrencyDataService, Currency, CoinValue } from './services/currency-data/currency-data.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, 
    IonicModule, 
    HeaderComponent, Sidenav,
    MatSidenavContainer, MatSidenavContent, 
    MatFormField, MatInput, MatSelect, MatOption, MatLabel],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, AfterViewInit {
  public apiUrl = env.apiUrl;
  pairs: string[] = [];
  confidences: { [key: string]: string } = {};
  lastTimestamps: { [key: string]: string } = {}; // Last timestamp for each pair
  dataLoaded = false;
  isDarkModeEnabled = true;
  selectedPair: string = "";
  chart: LightweightCharts.IChartApi | null = null;
  chartStyling: any;
  baseCurrencyMenu: Currency[] = [];
  secondCurrencyMenu: Currency[] = [];
  selectedBaseCurrency: any;
  selectedSecondCurrency: any;
  isChartDataSuccess: boolean = false;
  coinHistoryData: CoinValue[] = [];
  chartContainer: any;
  private resizeSubject: Subject<void> = new Subject();

  constructor(
    private currencyDataService: CurrencyDataService, 
    private chartDataService: ChartDataService
  ) {
    this.chartContainer = document.getElementById('chartContainer');
    this.resizeSubject.pipe(debounceTime(100)).subscribe(() => {
      this.chartDataService.adjustChartSize(this.chart, this.chartContainer);
    });
  }

  @HostListener('window:resize')
  onResize() {
    this.chartDataService.adjustChartSize(this.chart, this.chartContainer);
  }

  ngOnInit(): void {
    // this.setupBaseCurrencyDropdown();
    this.chartDataService.getChartDumps().subscribe(
      (dumps: any) => this.setupChart(dumps),
      (error) => {
        console.error('Error fetching chart data:', error);
        this.dataLoaded = false;
      }
    );
  }

  ngAfterViewInit(): void {
    if(this.dataLoaded) this.chartDataService.loadCharts(null, this.chart, this.pairs, this.selectedPair, this.lastTimestamps, this.isDarkModeEnabled); // Call loadCharts after view initialization
  }

  toggleDarkMode(): void {
    this.isDarkModeEnabled = !this.isDarkModeEnabled;
    this.chartDataService.loadCharts(null, this.chart, this.pairs, this.selectedPair, this.lastTimestamps, this.isDarkModeEnabled);
  }

  fetchCoinData = (): void => {
    const period = "7";
    this.currencyDataService.fetchCoinData(this.selectedBaseCurrency, this.selectedSecondCurrency, period).subscribe((data: any) => {
      this.isChartDataSuccess = true;
      this.coinHistoryData = data;
    })
  }

  setupBaseCurrencyDropdown = (): void => {
    const currencies_endpoint = `currencies`;
    this.currencyDataService.setupBaseCurrencyDropdown().subscribe((data: any) => {
      this.baseCurrencyMenu = data["res"];
      this.selectedBaseCurrency = data["res"][0]["code"];
      this.setupSecondCurrencyDropdown();
    })
  }

  setupSecondCurrencyDropdown = (): void => {
    this.currencyDataService.setupSecondCurrencyDropdown(this.selectedBaseCurrency).subscribe((data: any) => {
      this.secondCurrencyMenu = data["res"];
      this.selectedSecondCurrency = data["res"][1]["code"];
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

  setupChart(dumps: any) {
    this.pairs = dumps.map((dump: string) => this.chartDataService.cleanPair(dump));
    console.log('pairs', this.pairs);
    this.dataLoaded = true;
    this.chartDataService.loadCharts(null, this.chart, this.pairs, this.selectedPair, this.lastTimestamps, this.isDarkModeEnabled);
    this.pairs.forEach((pair) => {
      this.chartDataService.getConfidence(pair).subscribe(
        (confidence: any) => 
          this.confidences[pair] = confidence ?? 'default_value',
        (error) =>
          console.error(`Error fetching confidence for ${pair}:`, error)
      );
    });
  }

  loadCharts = (e: any) => this.chartDataService.loadCharts(null, this.chart, this.pairs, this.selectedPair, this.lastTimestamps, this.isDarkModeEnabled);
}