import { JsonPipe } from "@angular/common";

export interface JobSummary {
  id: string;
  note: string;
}

export interface JobHeader {
    id: string;
    sample: string;
    date: string;
    comment: string;
    configs: { [key: string]: string | number };
    axes: [];
    data_labels: [];
  }