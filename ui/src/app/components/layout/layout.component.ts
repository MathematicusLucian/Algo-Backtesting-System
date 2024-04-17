import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { CommonModule, NgFor } from '@angular/common';
import { MatSidenav, MatSidenavContainer, MatSidenavContent } from '@angular/material/sidenav';
import { BehaviorSubject, Observable, Subscription, map } from 'rxjs';
import { Store, select, Action } from '@ngrx/store';
import { ListState, selectItemClicked } from '../../state/list/list.state';
import { ClickListItem, CLICK_LIST_ITEM } from '../../state/list/list.actions';
import { ListReducer } from '../../state/list/list.reducers';
import List from '../../models/list.model';
import ActionWithPayload from '../../state/action-with-payload';
import { SideNavService } from '../../services/sidenav.service';
import { RouterOutlet } from '@angular/router';
import { MatIcon } from '@angular/material/icon';
import { ListComponent } from '../list/list.component';
// import { ShowSidenav } from '../../state/sidenav';

@Component({
  selector: 'prefab-layout',
  templateUrl: 'layout.component.html',
  styleUrl: 'layout.component.scss',
  standalone: true,
  imports: [CommonModule, ListComponent, RouterOutlet, NgFor, MatSidenav, MatSidenavContainer, MatSidenavContent, MatIcon],
})
export class LayoutComponent implements OnInit, OnChanges {
  @ViewChild('sidenav', {static: false}) public sidenav!: MatSidenav;
  @Input() pairs$: any = new BehaviorSubject<any[]>([]);
  pairs: any;
  @Input() selectedPair: string = "";
  @Input() open!: boolean | string;
  @Output() pairSelected = new EventEmitter<any>();
  ListState$!: Observable<string|null|undefined>;
  ListSubscription!: Subscription;
  ItemClicked: string|null|undefined = null;
  ListList!: List[];

  constructor(private sideNavService: SideNavService, private store: Store<ListState>) { }

  ngOnInit(){ 
    this.sideNavService.sideNavToggleSubject.subscribe(()=> this.sidenav.toggle());
    this.ListState$ = this.store.pipe(select(selectItemClicked));
    let clickListItemAction: ActionWithPayload<List> = {
      type: CLICK_LIST_ITEM,
      payload: { ItemClicked: null }
    }
    // this.store.dispatch(clickListItemAction);
    this.ListSubscription = this.ListState$.pipe(map(x => this.ItemClicked = x)).subscribe();
    this.store.dispatch(clickListItemAction);
  }

  ngOnChanges(changes: SimpleChanges): void {
    this.pairs = changes["pairs$"]["currentValue"];
  }

  selectPair(pair: string): void {
    this.selectedPair = pair;
    this.pairSelected.emit(this.selectedPair)
  }

  loadCharts = (e: any) => {
    let clickListItemAction: ActionWithPayload<List> = {
      type: CLICK_LIST_ITEM,
      payload: { ItemClicked: this.ItemClicked }
    }
    this.store.dispatch(clickListItemAction);
  }

  ngOnDestroy() {
    this.ListSubscription.unsubscribe();
}
}