import { Component, OnInit, AfterViewInit, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatSidenavModule } from '@angular/material/sidenav';

/** @title Implicit main content with two sidenavs */
@Component({
  selector: 'prefab-sidenav',
  templateUrl: 'sidenav.component.html',
  styleUrl: 'sidenav.component.scss',
  standalone: true,
  imports: [CommonModule, MatSidenavModule],
})
export class Sidenav {
  @Input() pairs: string[] = [];
  @Input() selectedPair: string = "";
  @Output() pairSelected = new EventEmitter<any>();
  @Input() open!: boolean | string;

  public isOpen = (): boolean => this.open === "true";

  selectPair(pair: string): void {
    this.selectedPair = pair;
    this.pairSelected.emit(this.selectedPair)
  }
}