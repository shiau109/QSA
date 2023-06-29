
import { AppComponent } from './app.component';

import { NgModule } from '@angular/core';

import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { MatAutocompleteModule } from "@angular/material/autocomplete";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { MessagesComponent } from './components/messages/messages.component';

import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { InMemoryDataService } from './in-memory-data.service';
import { SearchSampleComponent } from './components/search-sample/search-sample.component';
import { SampleDetailComponent } from './components/sample-detail/sample-detail.component';
import { JobListComponent } from './components/job-list/job-list.component';
import { SampleListComponent } from './components/sample-list/sample-list.component';
import { SearchComponent } from './components/search/search.component';
import { JobFilterComponent } from './components/job-filter/job-filter.component';

@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    MatAutocompleteModule, 
    JobFilterComponent,
    BrowserAnimationsModule,

// The HttpClientInMemoryWebApiModule module intercepts HTTP requests
// and returns simulated server responses.
// Remove it when a real server is ready to receive requests.
    // HttpClientInMemoryWebApiModule.forRoot(InMemoryDataService, { dataEncapsulation: false })
  ],
  declarations: [
    AppComponent,
    MessagesComponent,
    SearchSampleComponent,
    SampleDetailComponent,
    JobListComponent,
    SampleListComponent,
    SearchComponent,
    
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }