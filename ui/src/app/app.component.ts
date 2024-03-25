import {Component, OnInit} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import { Observable, of } from 'rxjs';

interface Season {
  season: string;
  url: string;
}

interface RoundsForSeason {
  circuitId: string,
  circuitName: string
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'F1 stats';
  season:any=null;
  selectedSeason: any;
  selectedRound: any;
  circuit:any=null;
  laps_for_round:any=null;
  BASE_URL = "http://localhost/api/";
  seasons_endpoint = "seasons";
  retrievedSeasons: Season[];
  retrievedRoundsForSeason: RoundsForSeason[];
  retrivedSeasonRoundData: any[];
  retrievedLapsForRound$: Observable<any> = of([]);
  isSeasonRoundDataSuccess: boolean = false;
  circuitData: any[]; 
  raceResults: any[];
  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.http.get<any>(this.BASE_URL+this.seasons_endpoint).subscribe(data => {
      this.retrievedSeasons = data;
      this.season = data[0];
      this.setupRoundsDropdown();
    })
  }

  setupRoundsDropdown(): void {
    const round_for_season_endpoint = `rounds_for_season?season=${this.season.season}`;
    // If time, would move this http function to a service
    this.http.get<any>(this.BASE_URL + round_for_season_endpoint).subscribe(data => {
      this.retrievedRoundsForSeason = data;
      this.circuit = data[0];
      this.setupDriverStandings();
      this.setupLaps();
    })
  }

  setupDriverStandings(): void {
    const round_results_endpoint = `round_results?season=${this.season.season}&round_no=${this.circuit.circuitId}`;
    this.http.get<any>(this.BASE_URL + round_results_endpoint).subscribe(data => {
      this.retrivedSeasonRoundData = data;
      this.isSeasonRoundDataSuccess = true;
      this.circuitData = data[0].Circuit ? data[0].Circuit : {};
      this.circuitData["circuitUrl"] = data[0].url ? data[0].url : "";
      this.raceResults = data[0].Results ? data[0].Results : {};
    })
  }

  setupLaps():void {
    const laps_for_round_endpoint = `laps_for_round?season=${this.season.season}&round_no=${this.circuit.circuitId}`;
    this.http.get<any>(this.BASE_URL + laps_for_round_endpoint).subscribe(data => {
      this.retrievedLapsForRound$ = of(data);
    })
  }

  selectSeason(event: Event): void {
    this.season.season = (event.target as HTMLSelectElement).value;
    this.setupRoundsDropdown();
  }

	selectRound(event: Event): void {
    this.circuit.circuitId = (event.target as HTMLSelectElement).value;
    this.setupDriverStandings();
    this.setupLaps();
	}
}
