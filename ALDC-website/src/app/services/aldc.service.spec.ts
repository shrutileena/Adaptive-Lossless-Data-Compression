import { TestBed } from '@angular/core/testing';

import { AldcService } from './aldc.service';

describe('AldcService', () => {
  let service: AldcService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AldcService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
