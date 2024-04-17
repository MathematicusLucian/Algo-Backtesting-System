import { Component, ElementRef, OnInit, AfterViewInit, ViewChild, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable, of } from 'rxjs';
import { DeepPartial, TimeChartOptions, ColorType, createChart } from 'lightweight-charts';
import * as LightweightCharts from 'lightweight-charts';
import { SeriesMarker } from 'lightweight-charts';
import { Time } from 'lightweight-charts';
import { ChartDataService } from './services/chart-data/chart-data.service';
import { Subject } from 'rxjs';
import { debounceTime } from 'rxjs/operators';
import { IonicModule } from '@ionic/angular';
import { MatFormField, MatLabel } from '@angular/material/form-field';
import { MatOption, MatSelect } from '@angular/material/select';
import { HeaderComponent } from './components/header/header.component';
import { MatInput } from '@angular/material/input';

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
  standalone: true,
  imports: [CommonModule, RouterOutlet, HeaderComponent, IonicModule, MatFormField, MatInput, MatSelect, MatOption, MatLabel],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit, AfterViewInit {
  title: string = "Market Tracker";
  pairs: string[] = [];
  confidences: { [key: string]: string } = {}; // Object to hold confidence values
  lastTimestamps: { [key: string]: string } = {}; // Object to hold the last timestamp for each pair
  dataLoaded = false; // Flag to check if data is loaded
  isDarkModeEnabled = true;
  selectedPair: string = "";
  chart: LightweightCharts.IChartApi | null = null;
  chartStyling: any;
  BASE_URL = "http://localhost/api/";
  baseCurrencyMenu: Currency[] = [];
  secondCurrencyMenu: Currency[] = [];
  selectedBaseCurrency: any;
  selectedSecondCurrency: any;
  isChartDataSuccess: boolean = false;
  coinHistoryData: CoinValue[] = [];
  private resizeSubject: Subject<void> = new Subject();
  private candleSeries: LightweightCharts.ISeriesApi<'Candlestick'> | null = null;
  private lineSeries: LightweightCharts.ISeriesApi<'Line'> | null = null;

  constructor(private http: HttpClient, private chartDataService: ChartDataService) {
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
    this.setupBaseCurrencyDropdown();
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

  selectPair(pair: string): void {
    this.selectedPair = pair;
    this.loadCharts();
  }

  loadCharts(): void {
    if (this.selectedPair != "") {
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
    if (!pair) return '';
    return pair.replace(/[^a-zA-Z0-9]/g, '');
  }

  formatDateToDDMMYYYYHHMM(date: any) {
    const day = ('0' + date.getDate()).slice(-2); // Add leading zero if needed
    const month = ('0' + (date.getMonth() + 1)).slice(-2); // Months are 0-indexed
    const year = date.getFullYear();
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);
    return `${day}-${month}-${year} ${hours}:${minutes}`;
  }

  destroyChart() {
    if (this.chart) {
      this.chart.remove(); // Clear the old chart before creating a new one
      this.chart = null;
    }
  }

  createChart(pair: string, data: any[]): void {
    this.destroyChart();
    const chartContainer = document.getElementById('chartContainer');
    if (!chartContainer) return;
    if (!this.chart) {
      this.chartStyling = {
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
      };
      this.chart = LightweightCharts.createChart(chartContainer, this.chartStyling);
    }
    
    // Assuming data is sorted and the last element is the latest
    if (data && data.length > 0) {
        const lastData = data[data.length - 1];
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

        if (this.candleSeries) // Ensure candleSeries is not null before setting markers
        this.candleSeries.setMarkers(markers);
      }
    });
  }

  toggleDarkMode(): void {
    this.isDarkModeEnabled = !this.isDarkModeEnabled;
    this.loadCharts();
  }

}