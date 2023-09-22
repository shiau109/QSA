
import { AppComponent } from './app.component';

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { BrowserModule } from '@angular/platform-browser';
// import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { MatAutocompleteModule } from "@angular/material/autocomplete";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import * as PlotlyJS from 'plotly.js-dist-min';
import { PlotlyModule } from 'angular-plotly.js';
PlotlyModule.plotlyjs = PlotlyJS;

import { MessagesComponent } from './components/messages/messages.component';

import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { SearchSampleComponent } from './components/search-sample/search-sample.component';
import { SampleDetailComponent } from './components/sample-detail/sample-detail.component';
import { SampleListComponent } from './components/sample-list/sample-list.component';
import { SearchComponent } from './components/search/search.component';
import { JobFilterComponent } from './components/job-filter/job-filter.component';
import { JobDetailComponent } from './components/job-detail/job-detail.component';
import { PlotRequestFormComponent } from './components/plot-request-form/plot-request-form.component';
import { AnalyzerHomeComponent } from './components/analyzer-home/analyzer-home.component';
import { ResonatorAnalysisComponent } from './components/resonator-analysis/resonator-analysis.component';
import { PreprocessRequestFormComponent } from './components/preprocess-request-form/preprocess-request-form.component';


@NgModule({
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    MatAutocompleteModule, 
    // JobFilterComponent,
    BrowserAnimationsModule,
    ReactiveFormsModule,
    PlotlyModule,
    CommonModule,
    ReactiveFormsModule,
    FormsModule
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
    SampleListComponent,
    SearchComponent,
    JobDetailComponent,
    JobFilterComponent,
    PlotRequestFormComponent,
    AnalyzerHomeComponent,
    ResonatorAnalysisComponent,
    PreprocessRequestFormComponent,
  ],
  bootstrap: [ AppComponent ]
})
export class AppModule { }