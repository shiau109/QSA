import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AnalyzerHomeComponent } from './analyzer-home.component';

describe('AnalyzerHomeComponent', () => {
  let component: AnalyzerHomeComponent;
  let fixture: ComponentFixture<AnalyzerHomeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AnalyzerHomeComponent]
    });
    fixture = TestBed.createComponent(AnalyzerHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
