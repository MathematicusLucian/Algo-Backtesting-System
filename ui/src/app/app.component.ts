import { Component, ElementRef, OnInit, AfterViewInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { DeepPartial, TimeChartOptions, ColorType, createChart } from 'lightweight-charts';
import { map } from 'rxjs/operators';
import { ChartDataService } from './services/chart-data/chart-data.service';
import * as LightweightCharts from 'lightweight-charts';
import { SeriesMarker } from 'lightweight-charts';
// import time from lightweight-charts
import { Time } from 'lightweight-charts';
import { HostListener } from '@angular/core';
import { Subject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [IonicModule, CommonModule, RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, AfterViewInit {
  title: string = "AlgoTrading";
  pairs: string[] = [];
  confidences: { [key: string]: string } = {}; // Object to hold confidence values
  lastTimestamps: { [key: string]: string } = {}; // Object to hold the last timestamp for each pair
  dataLoaded = false; // Flag to check if data is loaded
  isDarkModeEnabled = true;
  selectedPair: string = "";
  chart: LightweightCharts.IChartApi | null = null;
  private resizeSubject: Subject<void> = new Subject();
  private candleSeries: LightweightCharts.ISeriesApi<'Candlestick'> | null = null;
  private lineSeries: LightweightCharts.ISeriesApi<'Line'> | null = null;

  constructor(private chartDataService: ChartDataService) {
    this.resizeSubject.pipe(debounceTime(100)).subscribe(() => {
      this.adjustChartSize();
    });
  }

  @HostListener('window:resize')
  onResize() {
    this.adjustChartSize();
  }

  adjustChartSize(): void {
    const chartContainer = document.getElementById('chartContainer');
    if (chartContainer && this.chart) {
      // Directly adjust the chart size without additional DOM manipulations
      this.chart.resize(chartContainer.clientWidth, 400); // Keep a fixed height or adjust as needed
    }
  }

  ngOnInit(): void {
    this.chartDataService.getChartDumps().subscribe(
      (dumps: any) => {
        this.pairs = dumps.map((dump: string) => this.cleanPair(dump));
        this.dataLoaded = true; // Set flag to true after data is loaded
        this.loadCharts(); // Call loadCharts here after data is loaded

        // Get confidence for every pair
        this.pairs.forEach((pair) => {
          this.chartDataService.getConfidence(pair).subscribe(
            (confidence: any) => {
              console.log(`Confidence for ${pair}:`, confidence);
              this.confidences[pair] = confidence ?? 'default_value'; // Replace 'default_value' with a suitable fallback
            },
            (error) => {
              console.error(`Error fetching confidence for ${pair}:`, error);
            }
          );
        });
      },
      (error) => {
        console.error('Error fetching chart dumps:', error);
        this.dataLoaded = false;
      }
    );
  }

  ngAfterViewInit(): void {
    console.log(this.dataLoaded);
    if (this.dataLoaded) {
      this.loadCharts(); // Call loadCharts after view initialization
    }
  }

  fetchNewData(): void {
    this.chartDataService.getChartDumps().subscribe(
      (dumps: any) => {
        this.pairs = dumps.map((dump: string) => this.cleanPair(dump));
        // Reset existing data
        this.confidences = {};
        this.lastTimestamps = {};
        this.loadCharts(); // Load charts with new data
      },
      (error) => {
        console.error('Error fetching new chart dumps:', error);
      }
    );
  }

  selectPair(pair: string): void {
    this.selectedPair = pair;
    // Assuming loadCharts can now handle loading a single chart,
    // modify it accordingly if needed.
    this.loadCharts();
  }

  loadCharts(): void {
    // Adjust this method to either load all charts or just the one for selectedPair
    if (this.selectedPair != "") {
      // Load chart only for the selected pair
      this.chartDataService.getModelBars(this.selectedPair, 2000).subscribe((data: any) => {
        if (Array.isArray(data)) {
          this.createChart(this.selectedPair, data);
        }
      });
    } else {
    this.pairs.forEach((pair) => {
      this.chartDataService.getModelBars(pair, 2000).subscribe((data: any) => {
        if (Array.isArray(data)) {
          this.createChart(pair, data);
        }
      });
    });
  }
  }

  cleanPair(pair: string): string {
    // Check if pair is undefined or null
    if (!pair) {
      return ''; // Return an empty string or handle it as you see fit
    }
    return pair.replace(/[^a-zA-Z0-9]/g, '');
  }

  formatDateToDDMMYYYYHHMM(date: any) {
    const day = ('0' + date.getDate()).slice(-2); // Add leading zero if needed
    const month = ('0' + (date.getMonth() + 1)).slice(-2); // Months are 0-indexed
    const year = date.getFullYear();
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);

    // Formatting the date string as "dd-mm-yyyy hh:mm"
    return `${day}-${month}-${year} ${hours}:${minutes}`;
  }

  createChart(pair: string, data: any[]): void {
    const chartContainer = document.getElementById('chartContainer');
    // Clear the old chart before creating a new one
    if (this.chart) {
      this.chart.remove();
      this.chart = null;
    }
    if (!chartContainer) return;
    if (!this.chart) {
      this.chart = LightweightCharts.createChart(chartContainer, {
        width: chartContainer.clientWidth,
        height: 400,
        layout: {
          background: {
            type: LightweightCharts.ColorType.Solid,
            color: this.isDarkModeEnabled ? '#131722' : '#ffffff',
          },
          textColor: this.isDarkModeEnabled ? '#D9D9D9' : '#191919',
        },
        grid: {
          vertLines: { color: 'rgba(197, 203, 206, 0.5)' },
          horzLines: { color: 'rgba(197, 203, 206, 0.5)' },
        },
        crosshair: {
          mode: LightweightCharts.CrosshairMode.Normal,
        },
        rightPriceScale: {
          borderColor: 'rgba(197, 203, 206, 0.8)',
        },
        timeScale: {
          borderColor: 'rgba(197, 203, 206, 0.8)',
          timeVisible: true,
        },
      });
    }
    
    // Assuming data is sorted and the last element is the latest
    if (data && data.length > 0) {
        const lastData = data[data.length - 1];
        // Extract the last timestamp from the data
        const lastTimestamp = this.formatDateToDDMMYYYYHHMM(new Date(lastData.time * 1000));
        this.lastTimestamps[pair] = lastTimestamp;
    }

    // Check if candleSeries and lineSeries are null before creating new ones
    this.candleSeries = this.chart.addCandlestickSeries({
      upColor: 'rgba(0, 255, 255, 1)',
      downColor: 'rgba(255, 0, 0, 1)',
      borderDownColor: 'rgba(255, 0, 0, 1)',
      borderUpColor: 'rgba(0, 255, 255, 1)',
      wickDownColor: 'rgba(255, 0, 0, 1)',
      wickUpColor: 'rgba(0, 255, 255, 1)',
      priceFormat: {
        type: 'custom',
        formatter: (price: any) => price.toFixed(4),
      },
    });

    this.candleSeries.setData(
      data.map(d => ({
        time: d.time,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      }))
    );

    this.lineSeries = this.chart.addLineSeries({
      color: 'rgba(0, 150, 136, 1)',
      lineWidth: 2,
    });

    // This assumes you've ensured the data for predictions is loaded
    this.chartDataService.getPrediction(pair).subscribe(predictionData => {
      if (Array.isArray(predictionData)) {
        if(this.lineSeries)
        this.lineSeries.setData(
          predictionData.map(d => ({
            time: d.time,
            value: d.close,
          }))
        );
      }
    });

    this.chartDataService.getConfidences(pair).subscribe(confidenceData => {
      if (Array.isArray(confidenceData) && confidenceData.length > 0) {
        const markers: SeriesMarker<Time>[] = confidenceData.map(confidence => ({
          time: confidence.t,
          position: 'aboveBar',
          color: 'white',
          shape: 'arrowDown',
          text: confidence.value,
        }));

        // Ensure candleSeries is not null before setting markers
        if (this.candleSeries)
        this.candleSeries.setMarkers(markers);
      }
    });
  }

  toggleDarkMode(): void {
    this.isDarkModeEnabled = !this.isDarkModeEnabled;
    this.loadCharts();
  }
}

// import {Component, OnInit} from '@angular/core';
// import {HttpClient} from '@angular/common/http';
// import { Observable, of } from 'rxjs';

// interface Currency {
//   name: string;
//   code: string;
// }
// interface CoinValue {
//   date: string,
//   price: string
// }

// @Component({
//   selector: 'app-root',
//   templateUrl: './app.component.html',
//   styleUrls: ['./app.component.css']
// })
// export class AppComponent implements OnInit {
//   title = 'CryptoTracker';
//   BASE_URL = "http://localhost/api/";
//   baseCurrencyMenu: Currency[] = null;
//   secondCurrencyMenu: Currency[] = null;
//   selectedBaseCurrency: any;
//   selectedSecondCurrency: any;
//   isChartDataSuccess: boolean = false;
//   coinHistoryData: CoinValue[] = null;
//   constructor(private http: HttpClient) { }

//   ngOnInit(): void {
//     this.setupBaseCurrencyDropdown();
//   }

//   setupBaseCurrencyDropdown = (): void => {
//     const currencies_endpoint = `currencies`;
//     this.http.get<any>(this.BASE_URL + currencies_endpoint).subscribe(data => {
//       this.baseCurrencyMenu = data["res"];
//       this.selectedBaseCurrency = data["res"][0]["code"];
//       this.setupSecondCurrencyDropdown();
//     })
//   }

//   setupSecondCurrencyDropdown = (): void => {
//     const currencies_endpoint = `currencies?selected=${this.selectedBaseCurrency}`;
//     this.http.get<any>(this.BASE_URL + currencies_endpoint).subscribe(data => {
//       this.secondCurrencyMenu = data["res"];
//       this.selectedSecondCurrency = data["res"][1]["code"];
//     })
//   }

//   fetchCoinData = (): void => {
//     const period = "7";
//     const round_results_endpoint = `coin_history?base=${this.selectedBaseCurrency}&second_currency=${this.selectedSecondCurrency}&period=${period}`;
//     this.http.get<any>(this.BASE_URL + round_results_endpoint).subscribe(data => {
//       this.isChartDataSuccess = true;
//       this.coinHistoryData = data;
//     })
//   }

//   selectBaseCurrency = (event: Event): void => {
//     this.selectedBaseCurrency = (event.target as HTMLSelectElement).value;
//     this.setupSecondCurrencyDropdown();
//   }

// 	selectSecondCurrency = (event: Event): void => {
//     this.selectedSecondCurrency = (event.target as HTMLSelectElement).value;
//     this.fetchCoinData();
// 	}

// }


// <prefab-header></prefab-header>

// <div id="main">

//   <div *ngIf="baseCurrencyMenu?.length">

//     <mat-form-field>
//       <!-- <mat-label>Base:</mat-label> -->
//       <select matNativeControl (change)="selectBaseCurrency($event)">
//         @for (option of baseCurrencyMenu; track option) {
//           <option [value]="option.code" [selected]="selectedBaseCurrency === option.code">{{ option.name }}</option>
//         }
//       </select>
//     </mat-form-field>

//     <span>to</span>

//     <div id="menu-wrapper" *ngIf="secondCurrencyMenu?.length">

//       <mat-form-field>
//         <!-- <mat-label>Currency:</mat-label> -->
//         <select matNativeControl (change)="selectSecondCurrency($event)">
//           @for (option of secondCurrencyMenu; track option) {
//             <option [value]="option.code" [selected]="selectedSecondaryCurrency === option.code">{{ option.name }}</option>
//           }
//         </select>
//       </mat-form-field>

//     </div>

//   </div>

//   <!-- If time, would add a spinner -->
//   <h1 *ngIf="!isChartDataSuccess">Loading . . . </h1>

//   <div *ngIf="isChartDataSuccess">
      
//     <pre>{{coinHistoryData|json}}</pre>

//   </div>

// </div>