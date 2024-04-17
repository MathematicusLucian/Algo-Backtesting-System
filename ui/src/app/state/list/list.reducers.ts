import ActionWithPayload from "../action-with-payload";
import List from "../../models/list.model";
import { ListState, initializeState } from "./list.state";
import * as ListActions from "./list.actions";
import { Action } from "@ngrx/store";

const initialState = initializeState();

export function ListReducer(state: ListState = initialState, action: Action) {
    switch (action.type) {
        case ListActions.CLICK_LIST_ITEM:
            return ({
                ...state,
                ItemClicked: state.ItemClicked = (action as ActionWithPayload<List>).payload.ItemClicked,
            });
        default:
            return state;
    }
}