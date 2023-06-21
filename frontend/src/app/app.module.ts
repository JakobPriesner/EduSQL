import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { InitGameComponent } from './init-game/init-game.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {RouterOutlet} from "@angular/router";
import {MatToolbarModule} from "@angular/material/toolbar";
import {MatIconModule} from "@angular/material/icon";
import {MatButtonModule} from "@angular/material/button";
import {MatInputModule} from "@angular/material/input";
import {HttpClientModule} from "@angular/common/http";
import {MatSnackBarModule} from "@angular/material/snack-bar";
import {CommonModule, NgOptimizedImage} from "@angular/common";
import {MatProgressSpinnerModule} from "@angular/material/progress-spinner";
import {MatProgressBarModule} from "@angular/material/progress-bar";
import { GameComponent } from './game/game.component';
import {MatStepperModule} from "@angular/material/stepper";
import { LevelOneComponent } from './level-one/level-one.component';
import { ErmDialogComponent } from './erm-dialog/erm-dialog.component';
import {MatDialogModule} from "@angular/material/dialog";
import {NgxImageZoomModule} from "ngx-image-zoom";
import { AlertComponent } from './alert/alert.component';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MatFormFieldModule} from "@angular/material/form-field";
import { LoginComponent } from './login/login.component';
import {MatCardModule} from "@angular/material/card";
import { LevelTwoComponent } from './level-two/level-two.component';
import { CodeEditorComponent } from './code-editor/code-editor.component';
import { ValidateBtnComponent } from './validate-btn/validate-btn.component';
import { ValidationErrorsComponent } from './validation-errors/validation-errors.component';
import {FlexLayoutModule} from "@angular/flex-layout";
import { LevelThreeComponent } from './level-three/level-three.component';
import { LevelSevenComponent } from './level-seven/level-seven.component';
import { LevelEightComponent } from './level-eight/level-eight.component';
import { DbInteractionComponent } from './db-interaction/db-interaction.component';
import {MatTableModule} from "@angular/material/table";
import { LevelSixComponent } from './level-six/level-six.component';
import {MatSelectModule} from "@angular/material/select";
import {MatCheckboxModule} from "@angular/material/checkbox";
import { SelectAllResultTableComponent } from './db-interaction/select-all-result-table/select-all-result-table.component';
import {MatExpansionModule} from "@angular/material/expansion";
import {MatTabsModule} from "@angular/material/tabs";
import {LevelFourComponent} from "./level-four/level-four.component";
import { LevelTenComponent } from './level-ten/level-ten.component';
import {MonacoEditorModule} from "ngx-monaco-editor-v2";
import {LevelNineComponent} from "./level-nine/level-nine.component";
import {LevelElevenComponent} from "./level-eleven/level-eleven.component";
import { LevelTwelveComponent } from './level-twelve/level-twelve.component';
import { LevelFiveComponent } from './level-five/level-five.component';

@NgModule({
    declarations: [
        AppComponent,
        InitGameComponent,
        GameComponent,
        LevelOneComponent,
        ErmDialogComponent,
        AlertComponent,
        LoginComponent,
        LevelTwoComponent,
        CodeEditorComponent,
        ValidateBtnComponent,
        ValidationErrorsComponent,
        LevelThreeComponent,
        LevelSevenComponent,
        LevelEightComponent,
        DbInteractionComponent,
        LevelSixComponent,
        SelectAllResultTableComponent,
        LevelFourComponent,
        LevelTenComponent,
        LevelNineComponent,
        LevelElevenComponent,
        LevelTwelveComponent,
        LevelElevenComponent,
        LevelFiveComponent
    ],
    imports: [
        HttpClientModule,
        FormsModule,
        BrowserModule,
        BrowserAnimationsModule,
        CommonModule,
        RouterOutlet,
        MatToolbarModule,
        MatIconModule,
        MatButtonModule,
        MatInputModule,
        MatSnackBarModule,
        MatProgressSpinnerModule,
        MatProgressBarModule,
        MatStepperModule,
        MatDialogModule,
        NgxImageZoomModule,
        ReactiveFormsModule,
        MatFormFieldModule,
        MatCardModule,
        MonacoEditorModule.forRoot(),
        FlexLayoutModule,
        NgOptimizedImage,
        MatTableModule,
        MatSelectModule,
        MatCheckboxModule,
        MatExpansionModule,
        MatCheckboxModule,
        MatTabsModule
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
