import { Component, OnInit } from '@angular/core';
import { MatToolbar, MatToolbarModule, MatToolbarRow } from "@angular/material/toolbar";
import { MatIcon, MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'prefab-header',
  standalone: true,
  imports: [MatToolbar, MatToolbarRow, MatIcon],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {}

}
