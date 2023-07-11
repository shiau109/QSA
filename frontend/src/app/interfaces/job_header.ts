import { JsonPipe } from "@angular/common";

export interface JobHeader {
    id: string;
    sample: string;
    date: string;
    comment: string;
    configs: { [key: string]: string | number };
    axes: [];
    data_labels: [];
  }