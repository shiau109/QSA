import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SampleListComponent } from './sample-list.component';

describe('SampleListComponent', () => {
  let component: SampleListComponent;
  let fixture: ComponentFixture<SampleListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SampleListComponent]
    });
    fixture = TestBed.createComponent(SampleListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
