import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import {CookieService} from "../../lib/services/cookie.service";
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";

@Component({
  selector: 'app-level-ten',
  templateUrl: './level-ten.component.html',
  styleUrls: ['./level-ten.component.scss'],
  providers: [
      {
          provide: STEPPER_GLOBAL_OPTIONS,
          useValue: {showError: true},
      },
  ]
})
export class LevelTenComponent {
    public validationFormGroup: FormGroup;

    constructor(private formBuilder: FormBuilder,
                public cookieService: CookieService) {
        this.validationFormGroup = this.formBuilder.group({
            matriculationNumber: ['', Validators.required],
            averageGrade: ['', Validators.required]
        });
    }
}
