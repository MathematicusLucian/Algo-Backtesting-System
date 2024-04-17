import SideNav from "../../models/sidenav.model";

export interface SideNavState {
    Loading: boolean;
    Loaded: boolean;
    SideNavList: SideNav[];
}

export const initializeState = (): SideNavState => {
    return ({
        SideNavList: [],
        Loading: false,
        Loaded: true
    });
}