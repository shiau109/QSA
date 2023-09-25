import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SingleShotDistributionComponent } from './single-shot-distribution.component';

describe('SingleShotDistributionComponent', () => {
  let component: SingleShotDistributionComponent;
  let fixture: ComponentFixture<SingleShotDistributionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SingleShotDistributionComponent]
    });
    fixture = TestBed.createComponent(SingleShotDistributionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
