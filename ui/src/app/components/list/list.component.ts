import { Component, OnInit, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule, NgFor } from '@angular/common';
import { BehaviorSubject, Observable, Subscription } from 'rxjs';
import { Store, select, Action } from '@ngrx/store';
import { ListState, selectItemClicked } from '../../state/list/list.state';
import { ClickListItem, CLICK_LIST_ITEM } from '../../state/list/list.actions';
import { ListReducer } from '../../state/list/list.reducers';
import List from '../../models/list.model';
import ActionWithPayload from '../../state/action-with-payload';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'prefab-list',
  templateUrl: 'list.component.ts',
  styleUrl: 'list.component.scss',
  standalone: true,
  imports: [CommonModule, NgFor, MatIcon],
})
export class ListComponent implements OnInit, OnChanges {
  @Input() pairs$: any = new BehaviorSubject<any[]>([]);
  pairs: any;
  @Input() selectedPair: string = "";
  @Input() open!: boolean | string;
  ListState$!: Observable<string|null|undefined>;
  ListSubscription!: Subscription;
  ItemClicked: string|null|undefined = null;
  ListList!: List[];

  constructor(private store: Store<ListState>) { }

  ngOnInit(){ 
    let clickListItemAction: ActionWithPayload<List> = {
      type: CLICK_LIST_ITEM,
      payload: { ItemClicked: null }
    }
    this.store.dispatch(clickListItemAction);
}

  ngOnChanges(changes: SimpleChanges): void {
    this.pairs = changes["pairs$"]["currentValue"];
  }

  selectPair(pair: string): void {
    this.selectedPair = pair;
    let clickListItemAction: ActionWithPayload<List> = {
      type: CLICK_LIST_ITEM,
      payload: { ItemClicked: this.selectedPair }
    }
    this.store.dispatch(clickListItemAction);
  }

  ngOnDestroy() {
    this.ListSubscription.unsubscribe();
  }
}