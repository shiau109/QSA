import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PreprocessRequestFormComponent } from './preprocess-request-form.component';

describe('PreprocessRequestFormComponent', () => {
  let component: PreprocessRequestFormComponent;
  let fixture: ComponentFixture<PreprocessRequestFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PreprocessRequestFormComponent]
    });
    fixture = TestBed.createComponent(PreprocessRequestFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
