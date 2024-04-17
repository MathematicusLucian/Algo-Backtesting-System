import { Component, Injectable } from '@angular/core';
import { SideNavService } from '../../services/sidenav.service';
import { MatSidenav } from '@angular/material/sidenav';
import { MatToolbar, MatToolbarRow } from "@angular/material/toolbar";
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'prefab-header',
  standalone: true,
  imports: [ MatSidenav, MatToolbar, MatToolbarRow, MatIcon],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
// @Injectable({providedIn: 'root'})
export class HeaderComponent {
  title: string = "Dashboard";      

  constructor(private sideNavService: SideNavService) { } 

  clickMenu = () => this.sideNavService.toggle();
}