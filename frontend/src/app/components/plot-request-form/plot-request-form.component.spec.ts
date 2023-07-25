import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlotRequestFormComponent } from './plot-request-form.component';

describe('PlotRequestFormComponent', () => {
  let component: PlotRequestFormComponent;
  let fixture: ComponentFixture<PlotRequestFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PlotRequestFormComponent]
    });
    fixture = TestBed.createComponent(PlotRequestFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
