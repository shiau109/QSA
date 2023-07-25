import { TestBed } from '@angular/core/testing';

import { BackToPlotlyService } from './back-to-plotly.service';

describe('BackToPlotlyService', () => {
  let service: BackToPlotlyService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BackToPlotlyService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
