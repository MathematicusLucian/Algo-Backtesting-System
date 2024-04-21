import { Component, OnInit, Input, OnChanges, SimpleChanges, OnDestroy, ChangeDetectionStrategy } from '@angular/core';
import { CommonModule, NgFor } from '@angular/common';
import { BehaviorSubject, Observable, Subscription } from 'rxjs';
import { Store, select, Action } from '@ngrx/store';
import { ListState, selectItemClicked } from '../../state/list/list.state';
import { ClickListItem, CLICK_LIST_ITEM } from '../../state/list/list.actions';
// import { ListReducer } from '../../state/list/list.reducers';
import List from '../../models/list.model';
import ActionWithPayload from '../../state/action-with-payload';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'prefab-list',
  templateUrl: './list.component.html',
  styleUrl: './list.component.scss',
  standalone: true,
  imports: [CommonModule, NgFor, MatIcon],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class ListComponent implements OnInit, OnChanges, OnDestroy {
  @Input() selectedPair: string = "";
  @Input() open!: boolean | string;
  @Input() pairs$: any = new BehaviorSubject<any[]>([]);
  pairs: any;
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

  ngOnDestroy() {
    this.ListSubscription.unsubscribe();
  }

  selectPair(pair: string): void {
    this.selectedPair = pair;
    let clickListItemAction: ActionWithPayload<List> = {
      type: CLICK_LIST_ITEM,
      payload: { ItemClicked: this.selectedPair }
    }
    this.store.dispatch(clickListItemAction);
  }

}