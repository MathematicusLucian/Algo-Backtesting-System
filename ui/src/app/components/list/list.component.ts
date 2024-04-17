import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule, NgFor } from '@angular/common';
import { BehaviorSubject } from 'rxjs';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'prefab-list',
  template: `<h3>Pairs</h3>
  <div class="pair" *ngFor="let pair of pairs" (click)="selectPair(pair)" class="pair-selector">
      {{pair}}
  </div>`,
  styleUrl: 'list.component.scss',
  standalone: true,
  imports: [CommonModule, NgFor, MatIcon],
})
export class ListComponent implements OnInit, OnChanges {
  @Input() pairs$: any = new BehaviorSubject<any[]>([]);
  pairs: any;
  @Input() selectedPair: string = "";
  @Input() open!: boolean | string;
  @Output() pairSelected = new EventEmitter<any>();

  constructor() { }

  ngOnInit(){ }

  ngOnChanges(changes: SimpleChanges): void {
    this.pairs = changes["pairs$"]["currentValue"];
  }

  selectPair(pair: string): void {
    this.selectedPair = pair;
    this.pairSelected.emit(this.selectedPair)
  }
}