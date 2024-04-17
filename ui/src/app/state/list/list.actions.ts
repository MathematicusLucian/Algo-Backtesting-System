import { Action } from "@ngrx/store";
import ActionWithPayload from "../action-with-payload";
import List from "../../models/list.model";

export const CLICK_LIST_ITEM = '[List] CLICK_LIST_ITEM';

export class ClickListItem implements ActionWithPayload<List> {
    readonly type = CLICK_LIST_ITEM;
    payload: List;

    constructor(payload: List) {
        this.payload = payload;
    }
}

export type All = ClickListItem ;