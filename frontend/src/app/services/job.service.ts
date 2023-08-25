import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';

import { Sample } from '../interfaces/sample';
import { JobHeader, JobSummary } from '../interfaces/job_info';
import { 
  Plot1DFuncRequest, 
  PlotParEqRequest, 
  PlotContourRequest, 
  PreProcessRequest,
  PlotRequest } from '../interfaces/data_extract';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { catchError, map, tap } from 'rxjs/operators';
import { JobFilter } from '../interfaces/filter';

@Injectable({
  providedIn: 'root'
})
export class JobService {

  private dataUrl = 'http://localhost:7999';  // URL to web api
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  data!:JobHeader[];
  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  /** GET Jobs from the server */
  getJobs(): Observable<JobSummary[]> {
    // console.log(this.http.get(this.dataUrl) )
    return this.http.get<JobSummary[]>(this.dataUrl)
      .pipe(
        tap(_ => this.log('fetched heroes')),
        catchError(this.handleError<JobSummary[]>('getHeroes', []))
      );
      
  }

  /** GET job by jobid. Will 404 if jobid not found */
  getJobDetail(jobId: string): Observable<JobHeader> {
    const url = `${this.dataUrl}/job/${jobId}`;
    return this.http.get<JobHeader>(url).pipe(
      tap(_ => this.log(`fetched job ID =${jobId}`)),
      catchError(this.handleError<JobHeader>(`Job ID ${jobId} return error`))
    );
  }

  getJobPreview(jobId: string, pReq: PlotRequest, pProReq: PreProcessRequest[]): Observable<any> {
    const url = `${this.dataUrl}/job/${jobId}/preview`;
    console.log('service getJobPreview {pReq,pProReq}')
    return this.http.post<any>(url,{pReq,pProReq}).pipe(
      tap(_ => this.log(`fetched job ID =${jobId}`)),
      catchError(this.handleError<any>(`Job ID ${jobId} return error`))
    );
  }
  /** GET job by jobid. Request for Plot1DFunc Will 404 if jobid not found */
  getJob1Dpreview(jobId: string, pReq: Plot1DFuncRequest, pProReq: PreProcessRequest[]): Observable<any> {
    const url = `${this.dataUrl}/job/${jobId}/preview1D`;
    // console.log({pReq,pProReq})
    return this.http.post<any>(url,{pReq,pProReq}).pipe(
      tap(_ => this.log(`fetched job ID =${jobId}`)),
      catchError(this.handleError<any>(`Job ID ${jobId} return error`))
    );
  }

  /** GET job by jobid. Request for Plot1DFunc Will 404 if jobid not found */
  getJobPreviewParEq(jobId: string, pReq: PlotParEqRequest): Observable<any> {
    const url = `${this.dataUrl}/job/${jobId}/previewParEq`;
    return this.http.post<any>(url,pReq).pipe(
      tap(_ => this.log(`fetched job ID =${jobId}`)),
      catchError(this.handleError<any>(`Job ID PreviewParEq ${jobId} return error`))
    );
  }

  /** GET job by jobid. Request for Plot1DFunc Will 404 if jobid not found */
  getJobPreviewContour(jobId: string, pReq: PlotContourRequest): Observable<any> {
    const url = `${this.dataUrl}/job/${jobId}/previewContour`;
    return this.http.post<any>(url,pReq).pipe(
      tap(_ => this.log(`fetched job ID =${jobId}`)),
      catchError(this.handleError<any>(`Job ID previewContour ${jobId} return error`))
    );
  }
  /** Log a SampleService message with the MessageService */
  private log(message: string) {
    this.messageService.add(`SampleService: ${message}`);
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   *
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.log(`${operation} failed: ${error.message}`);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  /* GET samples whose serialNum contains search term */
  filterJobs( filter: JobFilter ): Observable<JobSummary[]> {
    // if (!filter.trim()) {
    //   // if not search term, return empty hero array.
    //   return of([]);
    // }
    // console.log(`${this.dataUrl}/search/job`)
    return this.http.post<any>(`${this.dataUrl}/search/job`,filter).pipe(
      tap(_ => this.log(`search`)),
      catchError(this.handleError<JobSummary[]>(`search error`))
    );
  }

}
