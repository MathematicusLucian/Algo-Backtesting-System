import { TestBed } from '@angular/core/testing';

import { CurrencyDataService } from './currency-data.service';

describe('CurrencyDataService', () => {
  let service: CurrencyDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CurrencyDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});