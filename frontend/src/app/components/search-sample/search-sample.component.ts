
import { Component, OnInit } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';

import { Sample } from 'src/app/interfaces/sample';
import { SampleService } from 'src/app/services/sample.service';
@Component({
  selector: 'app-search-sample',
  templateUrl: './search-sample.component.html',
  styleUrls: ['./search-sample.component.css']
})
export class SearchSampleComponent {
  samples$!: Observable<Sample[]>;
  private searchTerms = new Subject<string>();

  constructor(private sampleService: SampleService) { }

  // Push a search term into the observable stream.
  search(term: string): void {
    this.searchTerms.next(term);
  }

  ngOnInit(): void {
    this.samples$ = this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.sampleService.searchSamples(term)),
    );
  }
}
