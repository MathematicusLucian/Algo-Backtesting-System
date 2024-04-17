import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class SideNavService {
 public sideNavToggleSubject: BehaviorSubject<any> = new BehaviorSubject('toggle');

  constructor() { } 

  public toggle() {
    return this.sideNavToggleSubject.next('toggle');
  } 
}
