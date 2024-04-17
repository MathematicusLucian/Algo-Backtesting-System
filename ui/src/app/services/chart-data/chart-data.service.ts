import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { map } from 'rxjs/operators';
import { environment as env } from '../../../environments/environment';
import * as LightweightCharts from 'lightweight-charts';
import { SeriesMarker } from 'lightweight-charts';
import { Time } from 'lightweight-charts';

@Injectable({
  providedIn: 'root',
})
export class ChartDataService {
  private apiUrl = env.apiUrl;
  private candleSeries: LightweightCharts.ISeriesApi<'Candlestick'> | null = null;
  private lineSeries: LightweightCharts.ISeriesApi<'Line'> | null = null;

  constructor(private http: HttpClient) {}

  fetchNewData(chart: any, pairs: any, selectedPair: any, confidences: any, lastTimestamps: any, isDarkModeEnabled: any): void {
    this.getChartDumps().subscribe(
      (dumps: any) => {
        pairs = dumps.map((dump: string) => this.cleanPair(dump));
        confidences = {}; // Reset existing data
        lastTimestamps = {};
        this.loadCharts(null, chart, pairs, selectedPair, lastTimestamps, isDarkModeEnabled);
      },
      (error) => {
        console.error('Error fetching new chart dumps:', error);
      }
    );
  }

  loadCharts(e: any, chart: any, pairs: any, selectedPair: any, lastTimestamps: any, isDarkModeEnabled: any): void {
    console.log('selectedPair', selectedPair);
    if (selectedPair != "") {
      this.getModelBars(selectedPair, 2000).subscribe((data: any) => {
        if (Array.isArray(data)) {
          this.createChart(chart, selectedPair, data, lastTimestamps, isDarkModeEnabled);
        }
      });
    } else {
      console.log('pairs', pairs);
      pairs.forEach((pair: any) => {
        console.log('pair', pair);
        this.getModelBars(pair, 2000).subscribe((data: any) => {
          console.log('modelBars data', data);
          if (Array.isArray(data)) {
            this.createChart(chart, pair, data, lastTimestamps, isDarkModeEnabled);
          }
        });
      });
    }
  }

  updateCandleSeries = (chart: any, data: any) => {
    // Check if candleSeries and lineSeries are null before creating new ones
    let candleSeries = chart.addCandlestickSeries({
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
    candleSeries.setData(
      data.map((d: any) => ({
        time: d.time,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      }))
    );
    return candleSeries;
  }

  setPrediction(pair: any, lineSeries: any) {
    this.getPrediction(pair).subscribe(predictionData => { // Assumes ensured the data for predictions is loaded
      if (Array.isArray(predictionData)) {
        if(lineSeries)
        lineSeries.setData(
          predictionData.map(d => ({
            time: d.time,
            value: d.close,
          }))
        );
      }
    });
  }

  setConfidences(pair: any, candleSeries: any){
    this.getConfidences(pair).subscribe(confidenceData => {
      if (Array.isArray(confidenceData) && confidenceData.length > 0) {
        const markers: SeriesMarker<Time>[] = confidenceData.map(confidence => ({
          time: confidence.t,
          position: 'aboveBar',
          color: 'white',
          shape: 'arrowDown',
          text: confidence.value,
        }));
        if (candleSeries) candleSeries.setMarkers(markers);
      }
    });
  }

  createChart(chart: any, pair: string, data: any[], lastTimestamps: any, isDarkModeEnabled: any): void {
    this.destroyChart(chart);
    const chartContainer = document.getElementById('chartContainer');
    console.log('create chart', chartContainer);
    if (!chartContainer) return;
    if (!chart) {
      chart = LightweightCharts.createChart(chartContainer, this.createChartStyling(chartContainer, isDarkModeEnabled));
    } 
    console.log('create chart - 1', chart);
    console.log('create chart - data', data);
    if (data && data.length > 0) {    // Assuming data is sorted and the last element is the latest
        const lastData = data[data.length - 1];
        const lastTimestamp = this.formatDateToDDMMYYYYHHMM(new Date(lastData.time * 1000));
        lastTimestamps[pair] = lastTimestamp;
    }
    let candleSeries: LightweightCharts.ISeriesApi<'Candlestick'> | null = this.updateCandleSeries(chart, data);
    console.log('create chart - candleSeries', candleSeries);
    let lineSeries: LightweightCharts.ISeriesApi<'Line'> | null = chart.addLineSeries({
      color: 'rgba(0, 150, 136, 1)',
      lineWidth: 2,
    });
    console.log('create chart - lineSeries', lineSeries);
    this.setPrediction(pair, lineSeries);
    this.setConfidences(pair, candleSeries);
  }

  createChartStyling(chartContainer: any, isDarkModeEnabled: any) {
    return {
      width: chartContainer.clientWidth,
      height: 400,
      layout: {
        background: {
          type: LightweightCharts.ColorType.Solid,
          color: isDarkModeEnabled ? '#131722' : '#ffffff',
        },
        textColor: isDarkModeEnabled ? '#D9D9D9' : '#191919',
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
  }

  destroyChart = (chart: any) => {
    if(chart) {
      chart.remove();
      chart = null;
    }
  }
  adjustChartSize = (chart: any, chartContainer: any): void => {
    if(chartContainer && chart) chart.resize(chartContainer.clientWidth, 400);
  }
  cleanPair = (pair: string): string => (pair) ? pair.replace(/[^a-zA-Z0-9]/g, '') : '';
  getChartDumps = (): Observable<any>  => this.http.get(`${this.apiUrl}/dumps`);
  getConfidence = (pair: string): Observable<any> => this.http.get(`${this.apiUrl}/confidence/${pair}`);
  getConfidences = (pair: string): Observable<any> => this.http.get(`${this.apiUrl}/confidences/${pair}`);
  getModelBars = (pair: string, limit: number): Observable<any> => this.http
      .get(`${this.apiUrl}/bars/${pair}/${limit}`)
      .pipe(map((data) => this.adjustTimestamps(data)));
  getPrediction = (pair: string): Observable<any> => this.http
      .get(`${this.apiUrl}/prediction/${pair}`)
      .pipe(map((data) => this.adjustTimestamps(data)));

  private adjustTimestamps(data: any): any {
    const currentUtcOffset = this.getCurrentUtcOffsetInSeconds();
    if(data.data) {
      data.data = data.data.map((d: any) => ({
        ...d,
        time: d.time + currentUtcOffset,
      }));
    } else {
      return data.map((d: any) => ({
        ...d,
        time: d.time + currentUtcOffset,
      }));
    }
    return data;
  }

  formatDateToDDMMYYYYHHMM(date: any) {
    const day = ('0' + date.getDate()).slice(-2); // Add leading zero if needed
    const month = ('0' + (date.getMonth() + 1)).slice(-2); // Months are 0-indexed
    const year = date.getFullYear();
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);
    return `${day}-${month}-${year} ${hours}:${minutes}`;
  }

  // Get the current UTC offset in minutes and convert it to seconds
  // Note: getTimezoneOffset() returns the difference in minutes, negative for timezones ahead of UTC
  private getCurrentUtcOffsetInSeconds = (): number => -new Date().getTimezoneOffset() * 60;
}