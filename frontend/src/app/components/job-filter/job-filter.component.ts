import { Component, OnInit } from '@angular/core';
import { Observable, Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';

import {FormsModule, ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import {map, startWith} from 'rxjs/operators';
import {NgFor, AsyncPipe, NgIf} from '@angular/common';
import {MatAutocompleteModule} from '@angular/material/autocomplete';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';

import { Sample } from 'src/app/interfaces/sample';
import { SampleService } from 'src/app/services/sample.service';
import { JobFilter } from 'src/app/interfaces/filter';
import { JobService } from 'src/app/services/job.service';
import { JobSummary } from 'src/app/interfaces/job_info';
// export interface User {
//   name: string;
// }

@Component({
  selector: 'app-job-filter',
  templateUrl: './job-filter.component.html',
  styleUrls: ['./job-filter.component.css'],
  // imports: [
  //   FormsModule,
  //   MatFormFieldModule,
  //   MatInputModule,
  //   MatAutocompleteModule,
  //   ReactiveFormsModule,
  //   NgFor,
  //   AsyncPipe,
  //   NgIf,
    
  // ],
})
export class JobFilterComponent {

  options: string[] = [];
  filteredOptions!: Observable<string[]>;
  jobFilter! : FormGroup;
  JobSummaries!: JobSummary[];
  constructor(  private sampleService: SampleService,
                private fb: FormBuilder,
                private jobService: JobService) { }

  ngOnInit() {
    console.log('ngOnInit');
    this.jobFilter = this.fb.group({
      sn: [''],
      date: [''],
      htag: ['']
    });
    this.filteredOptions = this.jobFilter.controls['sn'].valueChanges.pipe(
      startWith(''),
      map((value) => {
        const name = value;
        return name ? this._filter(name as string) : this.options.slice();
      })
    );
  }
  onSubmit({ value, valid }: { value: JobFilter, valid: boolean }) {
    this.jobService.filterJobs(value).subscribe(data => {
      this.JobSummaries = data;
    });
    console.log(value, valid);

    console.log(this.JobSummaries);
  }
  // displayFn(user: string): string {
  //   console.log('displayFn', user);
  //   return user;
  // }

  private _filter(name: string): string[] {
    const filterValue = name.toLowerCase();
    console.log('_filter', filterValue);
    return this.options.filter((option) =>
      option.toLowerCase().includes(filterValue)
    );
  }
}
