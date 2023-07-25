import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResonatorAnalysisComponent } from './resonator-analysis.component';

describe('ResonatorAnalysisComponent', () => {
  let component: ResonatorAnalysisComponent;
  let fixture: ComponentFixture<ResonatorAnalysisComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ResonatorAnalysisComponent]
    });
    fixture = TestBed.createComponent(ResonatorAnalysisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
