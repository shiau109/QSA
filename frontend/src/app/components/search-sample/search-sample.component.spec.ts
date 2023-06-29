import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchSampleComponent } from './search-sample.component';

describe('SearchSampleComponent', () => {
  let component: SearchSampleComponent;
  let fixture: ComponentFixture<SearchSampleComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SearchSampleComponent]
    });
    fixture = TestBed.createComponent(SearchSampleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
