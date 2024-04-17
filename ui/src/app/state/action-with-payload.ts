import { Action } from "@ngrx/store";

export default interface ActionWithPayload<T> extends Action {
    payload: T;
}