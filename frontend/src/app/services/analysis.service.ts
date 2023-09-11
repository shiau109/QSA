import { Injectable } from '@angular/core';

import { Observable, of } from 'rxjs';

import { Sample } from '../interfaces/sample';
import { JobHeader, JobSummary } from '../interfaces/job_info';
import { 
  AnaRequest_resonator,
  PreProcessRequest
  } from '../interfaces/data_extract';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { catchError, map, tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AnalysisService {

  private dataUrl = 'http://192.168.1.135:7999';  // URL to web api
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };
  data!:JobHeader[];
  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  /** GET Jobs from the server */
  get_resonator_qfactor( prePro_req:PreProcessRequest, ana_req: AnaRequest_resonator ): Observable<JobSummary[]> {
    const url = `${this.dataUrl}/analysis/resonator_fit`;
    console.log({prePro_req, ana_req})
    return this.http.post<any>( url,{prePro_req, ana_req})
      .pipe(
        tap(_ => this.log('fetched analysis')),
        catchError(this.handleError<any>('get_resonator_qfactor', []))
      );
      
  }



  downloadAnalysisResult(jobId: string): Observable<any> {
    const url = `${this.dataUrl}/job/${jobId}/download/rawdata`;
    let httpOptions = { 
      observe: 'response' as 'body', 
      responseType: "blob" as "json"
    }
  
    console.log('service downloadJobRawdata');
   
    return this.http.post<any>(url,{},httpOptions).pipe(
      // res.set('Access-Control-Allow-Headers', '*');
      tap(_ => this.log(`fetched job ID =${jobId}`)),
      catchError(this.handleError<any>(`Job ID ${jobId} return error`))
    );
  };

  /** Log a SampleService message with the MessageService */
  private log(message: string) {
    this.messageService.add(`AnalysisService: ${message}`);
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


}
