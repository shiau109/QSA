import { ComponentFixture, TestBed } from '@angular/core/testing';

import { JobFilterComponent } from './job-filter.component';

describe('JobFilterComponent', () => {
  let component: JobFilterComponent;
  let fixture: ComponentFixture<JobFilterComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [JobFilterComponent]
    });
    fixture = TestBed.createComponent(JobFilterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
