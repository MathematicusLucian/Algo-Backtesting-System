import { Component, Injectable } from '@angular/core';

@Component({
  selector: 'prefab-dashboard',
  standalone: true,
  imports: [],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
// @Injectable({providedIn: 'root'})
export class DashboardComponent {
  title: string = "Dashboard";      

  constructor() { } 
}