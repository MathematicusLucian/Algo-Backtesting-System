import List from "../../models/list.model";

export interface ListState {
    ItemClicked: string | null | undefined;
}
export const initializeState = (): ListState => ({ ItemClicked: null });
export const selectItemClicked = (state: ListState) => state.ItemClicked;