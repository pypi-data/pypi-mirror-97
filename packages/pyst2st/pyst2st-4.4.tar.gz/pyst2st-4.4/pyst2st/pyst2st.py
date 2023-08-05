import math
from collections import defaultdict, OrderedDict
import inflect
from datetime import date
import pandas as pd

class StudentStory:
    def __init__(self, student_obj, **kwargs):
        self.choices = kwargs

        self.D_SCORED_INC_THRESHOLD = 6
        self.D_SCORED_DEC_THRESHOLD = -6
        self.PASS_INC_THRESHOLD = 9
        self.PASS_DEC_THRESHOLD = -9
        self.ATTEMPT_INC_THRESHOLD = 8
        self.ATTEMPT_DEC_THRESHOLD = -9
        self.FAIL_INC_THRESHOLD = 9
        self.FAIL_DEC_THRESHOLD = -6
        self.WITHDRAWN_INC_THRESHOLD = 7
        self.WITHDRAWN_DEC_THRESHOLD = -6
        self.GPA_INC_THRESHOLD = 2.11
        self.GPA_DEC_THRESHOLD = -2.3

        self.p = inflect.engine()

        self.data = student_obj
        self.semesters_list = self.data['semesters']
        self.sem_df, self.sem_with_summers_df, self.course_work, self.core_course_work, self.lowest_grade = self.get_semester_events()

        self.attempted_credits_count = self.sem_with_summers_df['attempted_count'].sum()
        self.passed_credits_count = self.sem_with_summers_df['passed_count'].sum()
        self.withdrawn_credits_count = self.sem_with_summers_df['withdrawn_count'].sum()
        self.failed_credits_count = self.sem_with_summers_df['failed_count'].sum()
        self.good_standing_sem_count = (self.sem_with_summers_df['academic_standing'] == "Good Standing").sum()
        self.probation_sem_count = (self.sem_with_summers_df['academic_standing'] == "Continued Probation").sum() + (self.sem_with_summers_df['academic_standing'] == "Probation").sum()
        self.suspended_academic_count = (self.sem_with_summers_df['academic_standing'] == "Suspended-Academic").sum() + (self.sem_with_summers_df['academic_standing'] == "Suspended-Academic-Reinstated").sum()
        self.passed_credits = ", ".join(self.sem_with_summers_df['passed_courses'])
        self.withdrawn_credits = ", ".join(self.sem_with_summers_df['withdrawn_courses'])
        self.attempted_credits = ", ".join(self.sem_with_summers_df['attempted_courses'])
        self.failed_credits = ", ".join(self.sem_with_summers_df['failed_courses'])
        self.d_credits_count = self.sem_with_summers_df['d_scored_count'].sum()
        self.d_scored_credits = ", ".join(self.sem_with_summers_df['d_scored_courses'])
        self.transferred_courses_count = self.sem_with_summers_df['transferred_count'].sum()
        self.transferred_courses = ", ".join(self.sem_with_summers_df['transferred_courses'])
        self.summer_semesters_count = (self.sem_with_summers_df['is_summer'] == 'yes').sum()
        self.advisor_count = int(self.sem_with_summers_df['advisor_count'].max())

        (self.first_semester_adv,self.first_advisor_period) = self.get_advisor_first_semester()
        (self.age_admitted, self.primary_ethnicity, self.gender,self.current_age) = self.get_demographic_data()
        self.student_name = self.data["name"]
        # If there is no first name in the database, we use last name instead in the stories
        self.first_name = self.data['first_name'] if len(self.data['first_name']) > 1 else self.data['last_name']
        self.last_name = self.data['last_name'] if self.first_name != self.data['last_name'] else ''
        (self.pronoun, self.pronoun_2, self.pronoun_3) = self.get_pronouns()
        self.major = self.get_major()
        self.enrollment_date = self.get_enrollment_date()
        self.semester_count = len(self.semesters_list) - self.summer_semesters_count
        self.expected_grad_date, self.tense = self.get_expected_grad()
        (self.grad_ind, self.graduation_date, self.last_semester_enrolled) = self.get_graduation_status()
        (self.gpa_ind, self.graduation_gpa) = self.get_gpa()
        (self.failed_course, self.semester_failed_course, self.new_grade_f,
         self.semester_passed_course_f) = self.get_failed_then_passed()
        (self.withdrawn_course, self.semester_withdrawn_course, self.new_grade_w, self.semester_passed_course_w) = self.get_withdrawn_then_passed()

        #         USER SELECTION WORK
        self.citizenship_desc = (self.data['background']['demographics']['citizenship_desc'] if type(
            self.data['background']['demographics']['citizenship_desc']) == str else "")
        if self.citizenship_desc == "United States Citizen":
            self.citizenship_desc = "United States"
        self.citizenship_type = (self.data['background']['demographics']['citizenship_type'] if type(
            self.data['background']['demographics']['citizenship_type']) == str else "")
        # self.current_age = (self.data['background']['demographics']['current_age'] if type(
        #     self.data['background']['demographics']['current_age']) == str else "")
        self.gender_desc = (self.data['background']['demographics']['gender_desc'] if type(
            self.data['background']['demographics']['gender_desc']) == str else "")
        self.nation_of_citizenship_desc = (
            self.data['background']['demographics']['nation_of_citizenship_desc'].strip() if type(
                self.data['background']['demographics']['nation_of_citizenship_desc']) == str and len(self.data['background']['demographics']['nation_of_citizenship_desc']) > 3 else "")
        if self.nation_of_citizenship_desc == '.': self.nation_of_citizenship_desc == ""
        self.primary_ethnicity_desc = (self.data['background']['demographics']['primary_ethnicity_desc'] if type(
            self.data['background']['demographics']['primary_ethnicity_desc']) == str else "")
        self.admission_population = self.get_admission_population()
        self.recent_gpa = self.get_recent_gpa()

        self.sig_fail_inc_dec_text = self.get_sig_fail_inc_dec_text()
        self.sig_pass_inc_dec_text = self.get_sig_pass_inc_dec_text()
        self.sig_attempt_inc_dec_text = self.get_sig_attempt_inc_dec_text()
        self.sig_withdrawn_inc_dec_text = self.get_sig_withdrawn_inc_dec_text()
        self.sig_gpa_inc_dec_text = self.get_sig_gpa_inc_dec_text()
        self.sig_d_scored_inc_dec_text = self.get_sig_d_scored_inc_dec_text()
        self.attempted_outliers_text = self.get_attempted_outliers_text()
        self.passed_outliers_text = self.get_passed_outliers_text()
        self.failed_outliers_text = self.get_failed_outliers_text()
        self.d_scored_outliers_text = self.get_d_scored_outliers_text()
        self.withdrawn_outliers_text = self.get_withdrawn_outliers_text()
        self.gpa_outliers_text = self.get_gpa_outliers_text()

        # CREATING STORY TEXTUAL CONTENT
        self.dem_text = self.get_dem_text()
        self.trans_text = self.get_trans_text()
        self.d_credits_text = self.get_d_credits_text()
        self.lowest_text = self.get_lowest_text()
        self.failed_then_passed_text = self.get_failed_then_passed_text()
        self.grad_text = self.get_grad_text()

        # DYNAMIC WORK
        self.credits_text = self.get_credits_text()

        self.temporal_story = []
        self.outcome_story = []
        self.default_story = []

        self.default_story.append({"docs": self.dem_text, "segment_name": "demo_text"})
        self.default_story.append({"docs": self.trans_text, "segment_name": "trans_text"})
        self.default_story.append({"docs": self.d_credits_text, "segment_name": "d_credits_text"})
        self.default_story.append({"docs": self.sig_attempt_inc_dec_text, "segment_name": "sig_attempt_inc_dec_text"})
        self.default_story.append({"docs": self.sig_pass_inc_dec_text, "segment_name": "sig_pass_inc_dec_text"})
        self.default_story.append({"docs": self.sig_fail_inc_dec_text, "segment_name": "sig_fail_inc_dec_text"})
        self.default_story.append({"docs": self.sig_withdrawn_inc_dec_text, "segment_name": "sig_withdrawn_inc_dec_text"})
        self.default_story.append({"docs": self.sig_d_scored_inc_dec_text, "segment_name": "sig_d_scored_inc_dec_text"})
        self.default_story.append({"docs": self.sig_gpa_inc_dec_text, "segment_name": "sig_gpa_inc_dec_text"})
        self.default_story.append({"docs": self.attempted_outliers_text, "segment_name": "attempted_outliers_text"})
        self.default_story.append({"docs": self.passed_outliers_text, "segment_name": "passed_outliers_text"})
        self.default_story.append({"docs": self.failed_outliers_text, "segment_name": "failed_outliers_text"})
        self.default_story.append({"docs": self.withdrawn_outliers_text, "segment_name": "withdrawn_outliers_text"})
        self.default_story.append({"docs": self.d_scored_outliers_text, "segment_name": "d_scored_outliers_text"})
        self.default_story.append({"docs": self.gpa_outliers_text, "segment_name": "gpa_outliers_text"})
        self.default_story.append({"docs": self.lowest_text, "segment_name": "lowest_text"})
        self.default_story.append({"docs": self.failed_then_passed_text, "segment_name": "failed_then_passed"})
        self.default_story.append({"docs": self.grad_text, "segment_name": "grad_text"})

        self.temporal_story = self.get_temporal_story()
        self.outcome_story = self.get_outcome_story()

    def get_last_sem_enrolled(self):
        def get_date(dt):
            dt = str(dt)
            semester_names = {
                1: "Spring",
                5: "First Summer",
                7: "Second Summer",
                8: "Fall"
            }
            return semester_names[int(dt[4:5])] + str(dt[:4])

        try:
            return get_date(self.data['grad_info']['last_semester_enrolled'])
        except:
            return ''

    def get_academic_standing_text(self):
        good_standing_sem_text = []
        probation_sem_text = []
        suspended_academic_text = []

        explanation = "You are seeing this in " + self.student_name + "\'s story because you have selected Academic Standing feature from the semester node."

        if self.good_standing_sem_count > 0:
            if self.good_standing_sem_count == 1:
                good_standing_sem_text = [
                    self.create_text(" in good academic standing for ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.good_standing_sem_count),"dynamic", "academic_standing_desc", "explanation"),
                    self.create_text(" semester", "template", None, "explanation"),
                ]
            else:
                good_standing_sem_text = [
                    self.create_text(" in good academic standing for ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.good_standing_sem_count),"dynamic", "academic_standing_desc", "explanation"),
                    self.create_text(" semesters", "template", None, "explanation"),
                ]
        if self.probation_sem_count > 0:
            if self.probation_sem_count == 1:
                probation_sem_text = [
                self.create_text(" on probation for ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.probation_sem_count),"dynamic", "academic_standing_desc", "explanation"),
                self.create_text(" semester", "template", None, "explanation"),
                ]
            else:
                probation_sem_text = [
                    self.create_text(" on probation for ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.probation_sem_count),"dynamic", "academic_standing_desc", "explanation"),
                    self.create_text(" semesters", "template", None, "explanation"),
                ]
        if self.suspended_academic_count > 0:
            if self.suspended_academic_count == 1:
                suspended_academic_text = [
                    self.create_text(" suspended for ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.suspended_academic_count),"dynamic", "academic_standing_desc", "explanation"),
                    self.create_text(" semester", "template", None, "explanation"),
                ]
            else:
                suspended_academic_text = [
                    self.create_text(" suspended for ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.suspended_academic_count),"dynamic", "academic_standing_desc", "explanation"),
                    self.create_text(" semesters", "template", None, "explanation"),
                ]

        comma_text = [self.create_text(",", "template", None, "explanation")]
        dot_text = [self.create_text(". ", "template", None, "explanation")]
        and_text = [self.create_text(" and", "template", None, "explanation")]
        academic_standing_text = [
            self.create_text("During ", "template", None, "explanation"),
            self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
            self.create_text(" enrollment, ", "template", None, "explanation"),
            self.create_text(self.first_name, "template", "first_name", "explanation"),
            self.create_text(" was", "template", None, "explanation"),
        ]

        if self.good_standing_sem_count > 0 and self.probation_sem_count == 0 and self.suspended_academic_count == 0:
            academic_standing_text = academic_standing_text + \
                good_standing_sem_text + dot_text
        elif self.good_standing_sem_count > 0 and self.probation_sem_count > 0 and self.suspended_academic_count == 0:
            academic_standing_text = academic_standing_text + \
                good_standing_sem_text + and_text + probation_sem_text + dot_text
        elif self.good_standing_sem_count > 0 and self.probation_sem_count == 0 and self.suspended_academic_count > 0:
            academic_standing_text = academic_standing_text + \
                good_standing_sem_text + and_text + suspended_academic_text + dot_text
        elif self.good_standing_sem_count > 0 and self.probation_sem_count > 0 and self.suspended_academic_count > 0:
            academic_standing_text = academic_standing_text + good_standing_sem_text + \
                comma_text + probation_sem_text + and_text + suspended_academic_text + dot_text
        elif self.good_standing_sem_count == 0 and self.probation_sem_count > 0 and self.suspended_academic_count == 0:
            academic_standing_text = academic_standing_text + probation_sem_text + dot_text
        elif self.good_standing_sem_count == 0 and self.probation_sem_count > 0 and self.suspended_academic_count > 0:
            academic_standing_text = academic_standing_text + \
                probation_sem_text + and_text + suspended_academic_text + dot_text
        elif self.good_standing_sem_count == 0 and self.probation_sem_count == 0 and self.suspended_academic_count > 0:
            academic_standing_text = academic_standing_text + \
                suspended_academic_text + dot_text
        else:
            academic_standing_text = [self.create_text("", "template", None, "explanation")]

        return academic_standing_text

    def get_adv_text(self):
        adv_text = [self.create_text("", "template", None, "explanation")]
        if self.advisor_count == 0:
            adv_text = [
                self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                self.create_text(" had never assigned an advisor throughout ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" enrollment. ", "template", None, "explanation"),
            ]
        elif self.advisor_count == 1:
            adv_text = [
                self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                self.create_text(" had only ", "template", None, "explanation"),
                self.create_text("one","dynamic", "advisor_count", "explanation"),
                self.create_text(" advisor throughout ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" enrollment. ", "template", None, "explanation"),
            ]
        else:
            adv_text = [
                self.create_text("Throughout ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender_desc", "explanation"),
                self.create_text(" enrollment, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                self.create_text(" has ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.advisor_count),"dynamic", "advisor_count", "explanation"),
                self.create_text(" advisors and ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender_desc", "explanation"),
                self.create_text(" had assigned ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender_desc", "explanation"),
                self.create_text(" first advisor in ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender_desc", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.first_semester_adv,"dynamic", "advisor_count", "explanation"),
                self.create_text(" semester in ", "template", None, "explanation"),
                self.create_text(self.first_advisor_period,"dynamic", "advisor_count", "explanation"),
                self.create_text(". ", "template", None, "explanation")
            ]
        return adv_text

    def get_temporal_story(self):
        #         Initialize all here!
        temporal_story = []
        academic_standing_text = [self.create_text("", "template", None, "explanation")]
        adv_text = [self.create_text("", "template", None, "explanation")]
        credits_text = [self.create_text("", "template", None, "explanation")]
        specific_dem_text = [self.create_text("", "template", None, "explanation")]
        academic_standing_text = [self.create_text("", "template", None, "explanation")]

        if self.choices['Academic standing'] == 'Yes': academic_standing_text = self.get_academic_standing_text()
        if self.choices['Advisor count'] == 'Yes':
            adv_text = self.get_adv_text()
        specific_dem_text = self.get_specific_dem_text()
        if 'Yes' in [self.choices['Credits attempted'], self.choices['Credits passed']]:
            credits_text = self.credits_text

        if 'Yes' in [self.choices['Credits attempted'], self.choices['Credits passed']]:
            credits_text = self.credits_text

        temporal_story.append({"docs": specific_dem_text, "segment_name": "specific_demo_text"})
        if self.choices["Credits transferred"] == "Yes": temporal_story.append({"docs": self.trans_text, "segment_name": "trans_text"})
        temporal_story.append({"docs": credits_text, "segment_name": "credits_text"})
        temporal_story.append({"docs": self.d_credits_text, "segment_name": "d_credits_text"})
        if self.choices["Credits attempted significant change"] == "Yes": temporal_story.append({"docs": self.sig_attempt_inc_dec_text, "segment_name": "sig_attempt_inc_dec_text"})
        if self.choices["Credits passed significant change"] == "Yes": temporal_story.append({"docs": self.sig_pass_inc_dec_text, "segment_name": "sig_pass_inc_dec_text"})
        if self.choices["Credits failed significant change"] == "Yes": temporal_story.append({"docs": self.sig_fail_inc_dec_text, "segment_name": "sig_fail_inc_dec_text"})
        if self.choices["Credits withdrawn significant change"] == "Yes": temporal_story.append({"docs": self.sig_withdrawn_inc_dec_text, "segment_name": "sig_withdrawn_inc_dec_text"})
        if self.choices["D-graded credits significant change"] == "Yes": temporal_story.append({"docs": self.sig_d_scored_inc_dec_text, "segment_name": "sig_d_scored_inc_dec_text"})
        if self.choices["GPA significant change"] == "Yes": temporal_story.append({"docs": self.sig_gpa_inc_dec_text, "segment_name": "sig_gpa_inc_dec_text"})
        if self.choices["Credits attempted outlier"] == "Yes": temporal_story.append({"docs": self.attempted_outliers_text, "segment_name": "attempted_outliers_text"})
        if self.choices["Credits passed outlier"] == "Yes": temporal_story.append({"docs": self.passed_outliers_text, "segment_name": "passed_outliers_text"})
        if self.choices["Credits failed outlier"] == "Yes": temporal_story.append({"docs": self.failed_outliers_text, "segment_name": "failed_outliers_text"})
        if self.choices["Credits withdrawn outlier"] == "Yes": temporal_story.append({"docs": self.withdrawn_outliers_text, "segment_name": "withdrawn_outliers_text"})
        if self.choices["GPA outlier"] == "Yes": temporal_story.append({"docs": self.gpa_outliers_text, "segment_name": "gpa_outliers_text"})
        if self.choices["D-graded credits outlier"] == "Yes": temporal_story.append({"docs": self.d_scored_outliers_text, "segment_name": "d_scored_outliers_text"})
        temporal_story.append({"docs": adv_text, "segment_name": "adv_text"})
        temporal_story.append({"docs": self.lowest_text, "segment_name": "lowest_text"})
        temporal_story.append({"docs": self.failed_then_passed_text, "segment_name": "failed_then_passed"})
        temporal_story.append({"docs": academic_standing_text, "segment_name": "academic_standing_text"})
        temporal_story.append({"docs": self.grad_text, "segment_name": "grad_text"})
        return temporal_story

    def get_outcome_story(self):
        outcome_story = []
        outcome_intro_text = [self.create_text("", "template", None, "explanation")]
        adv_text = [self.create_text("", "template", None, "explanation")]
        credits_text = [self.create_text("", "template", None, "explanation")]
        specific_dem_text = [self.create_text("", "template", None, "explanation")]

        academic_standing_text = [self.create_text("", "template", None, "explanation")]

        if self.choices['Academic standing'] == 'Yes': academic_standing_text = self.get_academic_standing_text()
        if self.choices['Advisor count'] == 'Yes':
            adv_text = self.get_adv_text()
        specific_dem_text = self.get_specific_dem_text()

        if 'Yes' in [self.choices['Credits attempted'], self.choices['Credits passed']]:
            credits_text = self.credits_text

        if self.grad_ind == False and self.expected_grad_date != "":
            if self.tense == 'future':
                outcome_intro_text = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" ", "template", None, "explanation"),
                    self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.gender,"dynamic", "gender", "explanation"),
                    self.create_text(" student who has not graduated yet and the last semester ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is eligible to apply for financial aid is ", "template", None, "explanation"),
                    self.create_text(self.expected_grad_date,"dynamic", "expected_grad_date", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.tense == 'past':
                outcome_intro_text = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" ", "template", None, "explanation"),
                    self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.gender,"dynamic", "gender", "explanation"),
                    self.create_text(" student who has not graduated yet while ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" was expected to graduate in ", "template", None, "explanation"),
                    self.create_text(self.expected_grad_date,"dynamic", "expected_grad_date", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            # if self.choices['gpa'] == 'Yes' and str(self.recent_gpa) != 'nan':
            outcome_intro_text += [
                self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                self.create_text(" latest cumulative GPA is ", "template", None, "explanation"),
                self.create_text(str(self.recent_gpa),"dynamic", "CGPA", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]
        elif self.grad_ind == False and self.expected_grad_date == "":
            outcome_intro_text = [
                self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                self.create_text(" is a ", "template", None, "explanation"),
                self.create_text(self.gender,"dynamic", "gender", "explanation"),
                self.create_text(" student who has not graduated yet and there is no information about ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" expected graduation date. ", "template", None, "explanation"),
            ]
            # if self.choices['gpa'] == 'Yes' and str(self.recent_gpa) != 'nan':
            outcome_intro_text += [
                self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                self.create_text(" latest cumulative GPA is ", "template", None, "explanation"),
                self.create_text(str(self.recent_gpa),"dynamic", "CGPA", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]
        elif self.grad_ind:
            outcome_intro_text = [
                self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                self.create_text(" is a ", "template", None, "explanation"),
                self.create_text(self.gender,"dynamic", "gender", "explanation"),
                self.create_text(" student who was graduated in ", "template", None, "explanation"),
                self.create_text(self.graduation_date,"dynamic", "graduation_date", "explanation"),
                self.create_text(" with a GPA of ", "template", None, "explanation"),
                self.create_text(str(self.graduation_gpa),"dynamic", "graduation_gpa", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]

        # academic_standing_text = self.get_academic_standing_text()
        specific_intro_text = self.get_specific_intro_text()

        outcome_story.append({"docs": outcome_intro_text, "segment_name": "outcome_intro_text"})
        outcome_story.append({"docs": specific_intro_text, "segment_name": "specific_intro_text"})
        outcome_story.append({"docs": academic_standing_text, "segment_name": "academic_standing_text"})
        if self.choices["Credits transferred"] == "Yes": outcome_story.append({"docs": self.trans_text, "segment_name": "trans_text"})
        outcome_story.append({"docs": credits_text, "segment_name": "credits_text"})
        outcome_story.append({"docs": self.d_credits_text, "segment_name": "d_credits_text"})
        if self.choices["Credits attempted significant change"] == "Yes": outcome_story.append({"docs": self.sig_attempt_inc_dec_text, "segment_name": "sig_attempt_inc_dec_text"})
        if self.choices["Credits passed significant change"] == "Yes": outcome_story.append({"docs": self.sig_pass_inc_dec_text, "segment_name": "sig_pass_inc_dec_text"})
        if self.choices["Credits failed significant change"] == "Yes": outcome_story.append({"docs": self.sig_fail_inc_dec_text, "segment_name": "sig_fail_inc_dec_text"})
        if self.choices["Credits withdrawn significant change"] == "Yes": outcome_story.append({"docs": self.sig_withdrawn_inc_dec_text, "segment_name": "sig_withdrawn_inc_dec_text"})
        if self.choices["D-graded credits significant change"] == "Yes": outcome_story.append({"docs": self.sig_d_scored_inc_dec_text, "segment_name": "sig_d_scored_inc_dec_text"})
        if self.choices["GPA significant change"] == "Yes": outcome_story.append({"docs": self.sig_gpa_inc_dec_text, "segment_name": "sig_gpa_inc_dec_text"})
        if self.choices["Credits attempted outlier"] == "Yes": outcome_story.append({"docs": self.attempted_outliers_text, "segment_name": "attempted_outliers_text"})
        if self.choices["Credits passed outlier"] == "Yes": outcome_story.append({"docs": self.passed_outliers_text, "segment_name": "passed_outliers_text"})
        if self.choices["Credits failed outlier"] == "Yes": outcome_story.append({"docs": self.failed_outliers_text, "segment_name": "failed_outliers_text"})
        if self.choices["Credits withdrawn outlier"] == "Yes": outcome_story.append({"docs": self.withdrawn_outliers_text, "segment_name": "withdrawn_outliers_text"})
        if self.choices["GPA outlier"] == "Yes": outcome_story.append({"docs": self.gpa_outliers_text, "segment_name": "gpa_outliers_text"})
        if self.choices["D-graded credits outlier"] == "Yes": outcome_story.append({"docs": self.d_scored_outliers_text, "segment_name": "d_scored_outliers_text"})
        outcome_story.append({"docs": adv_text, "segment_name": "adv_text"})
        outcome_story.append({"docs": self.lowest_text, "segment_name": "lowest_text"})
        outcome_story.append({"docs": self.failed_then_passed_text, "segment_name": "failed_then_passed"})
        return outcome_story

    def get_advisor_first_semester(self):
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        first_semester_adv = 1000
        for index, sem in enumerate(self.data['semesters'], 1):
            try:
                if sem['semesterInfo']['advisor_count'] > 0.0:
                    return (str(index) + suffix(index), sem['semesterInfo']['academic_period_desc'])
            except:
                return ("", "")
        return ("", "")

    def get_recent_gpa(self):
        return round(self.data['semesters'][-1]['semesterInfo']['CGPA'], 1)

    def get_attempted_outliers_text(self):
        attempted_outliers_text = [self.create_text("", "template", None, "explanation")]
        if self.semester_count < 4:
            return attempted_outliers_text
        outlier = self.data['sem_sequence_outliers']['attempted_credits_outliers']['anomaly']

        if outlier == 1:
            col_exceptions = ['student_id', 'cluster', 'anomaly']
            seq = [int(v) for k, v in self.data['sem_sequence_outliers']['attempted_credits_outliers'].items() if k not in col_exceptions]
            comma_sep_seq = ', '.join(str(it) for it in seq[:-1]) + ', and ' + str(seq[-1])
            explanation = "You might be interested in " + self.first_name + "\'s number of credit hours attempted each semester; in which " + self.pronoun.lower() + " shows an unusual pattern compared to the majority of students in CCI."

            attempted_outliers_text = [
                self.create_text("Compared to other students in CCI, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text(" follows a nontypical pattern for the number of credits attempted each semester, in which, during ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(len(seq)),"dynamic", "attempted_analysis", "explanation"),
                self.create_text(" enrolled semesters, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" attempted ", "template", None, "explanation"),
                self.create_text(comma_sep_seq,"dynamic", "attempted_analysis", explanation),
                self.create_text(" credit hours respectively. ", "template", None, "explanation")
            ]

        return attempted_outliers_text

    def get_passed_outliers_text(self):
        passed_outliers_text = [self.create_text("", "template", None, "explanation")]
        if self.semester_count < 4:
            return passed_outliers_text
        outlier = self.data['sem_sequence_outliers']['passed_credits_outliers']['anomaly']
        if outlier == 1:
            col_exceptions = ['student_id', 'cluster', 'anomaly']
            seq = [int(v) for k, v in self.data['sem_sequence_outliers']['passed_credits_outliers'].items() if k not in col_exceptions]
            comma_sep_seq = ', '.join(str(it) for it in seq[:-1]) + ', and ' + str(seq[-1])

            explanation = "You might be interested in " + self.first_name + "\'s number of credit hours passed each semester; in which " + self.pronoun.lower() + " shows an unusual pattern compared to the majority of students in CCI."

            passed_outliers_text = [
                self.create_text("Compared to other students in CCI, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text(" follows a nontypical pattern for the number of credits passed each semester, in which, during ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(len(seq)),"dynamic", "passed_analysis", "explanation"),
                self.create_text(" enrolled semesters, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" passed ", "template", None, "explanation"),
                self.create_text(comma_sep_seq,"dynamic", "passed_analysis", explanation),
                self.create_text(" credit hours respectively. ", "template", None, "explanation")
            ]

        return passed_outliers_text

    def get_failed_outliers_text(self):
        failed_outliers_text = [self.create_text("", "template", None, "explanation")]
        if self.semester_count < 4:
            return failed_outliers_text
        outlier = self.data['sem_sequence_outliers']['failed_credits_outliers']['anomaly']
        if outlier == 1:
            col_exceptions = ['student_id', 'cluster', 'anomaly']
            seq = [int(v) for k, v in self.data['sem_sequence_outliers']['failed_credits_outliers'].items() if k not in col_exceptions]
            comma_sep_seq = ', '.join(str(int(it)) for it in seq[:-1]) + ', and ' + str(int(seq[-1]))

            explanation = "You might be interested in " + self.first_name + "\'s number of credit hours failed each semester; in which " + self.pronoun.lower() + " shows an unusual pattern compared to the majority of students in CCI."

            failed_outliers_text = [
                self.create_text("Compared to other students in CCI, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text(" follows a nontypical pattern for the number of credits failed each semester, in which, during ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(len(seq)),"dynamic", "failed_analysis", "explanation"),
                self.create_text(" enrolled semesters, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" failed ", "template", None, "explanation"),
                self.create_text(comma_sep_seq,"dynamic", "failed_analysis", explanation),
                self.create_text(" credit hours respectively. ", "template", None, "explanation")
            ]

        return failed_outliers_text

    def get_d_scored_outliers_text(self):
        d_scored_outliers_text = [self.create_text("", "template", None, "explanation")]
        if self.semester_count < 4:
            return d_scored_outliers_text
        outlier = self.data['sem_sequence_outliers']['d_scored_credits_outliers']['anomaly']
        if outlier == 1:
            col_exceptions = ['student_id', 'cluster', 'anomaly']
            seq = [int(v) for k, v in self.data['sem_sequence_outliers']['d_scored_credits_outliers'].items() if k not in col_exceptions]
            comma_sep_seq = ', '.join(str(int(it)) for it in seq[:-1]) + ', and ' + str(int(seq[-1]))

            explanation = "You might be interested in " + self.first_name + "\'s number of credit hours with a D score each semester; in which " + self.pronoun.lower() + " shows an unusual pattern compared to the majority of students in CCI."

            d_scored_outliers_text = [
                self.create_text("Compared to other students in CCI, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text(" follows a nontypical pattern for the number of credits with a D score each semester, in which, during ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(len(seq)),"dynamic", "d_scored_analysis", "explanation"),
                self.create_text(" enrolled semesters, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" scored D in ", "template", None, "explanation"),
                self.create_text(comma_sep_seq,"dynamic","d_scored_analysis", explanation),
                self.create_text(" credit hours respectively. ", "template", None, "explanation")
            ]

        return d_scored_outliers_text

    def get_withdrawn_outliers_text(self):
        withdrawn_outliers_text = [self.create_text("", "template", None, "explanation")]
        if self.semester_count < 4:
            return withdrawn_outliers_text
        outlier = self.data['sem_sequence_outliers']['withdrawn_credits_outliers']['anomaly']
        if outlier == 1:
            col_exceptions = ['student_id', 'cluster', 'anomaly']
            seq = [int(v) for k, v in self.data['sem_sequence_outliers']['withdrawn_credits_outliers'].items() if k not in col_exceptions]
            comma_sep_seq = ', '.join(str(int(it)) for it in seq[:-1]) + ', and ' + str(int(seq[-1]))

            explanation = "You might be interested in " + self.first_name + "\'s number of credit hours withdrawn each semester; in which " + self.pronoun.lower() + " shows an unusual pattern compared to the majority of students in CCI."

            withdrawn_outliers_text = [
                self.create_text("Compared to other students in CCI, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text(" follows a nontypical pattern for the number of credits withdrawn each semester, in which, during ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(len(seq)),"dynamic", "withdrawn_analysis", "explanation"),
                self.create_text(" enrolled semesters, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" withdrew ", "template", None, "explanation"),
                self.create_text(comma_sep_seq,"dynamic","withdrawn_analysis", explanation),
                self.create_text(" credit hours respectively. ", "template", None, "explanation")
            ]

        return withdrawn_outliers_text

    def get_gpa_outliers_text(self):
        gpa_outliers_text = [self.create_text("", "template", None, "explanation")]
        if self.semester_count < 4:
            return gpa_outliers_text
        outlier = self.data['sem_sequence_outliers']['gpa_outliers']['anomaly']
        if outlier == 1:
            col_exceptions = ['student_id', 'cluster', 'anomaly']
            seq = [v for k, v in self.data['sem_sequence_outliers']['gpa_outliers'].items() if k not in col_exceptions]
            if all(i >= 2.5 for i in seq):
                return gpa_outliers_text

            comma_sep_seq = ', '.join(str(int(it)) for it in seq[:-1]) + ', and ' + str(int(seq[-1]))

            explanation = "You might be interested in " + self.first_name + "\'s GPA each semester; in which " + self.pronoun.lower() + " shows an unusual pattern compared to the majority of students in CCI."

            gpa_outliers_text = [
                self.create_text("Compared to other students in CCI, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text(" follows a nontypical pattern for the GPA each semester, in which, during ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(len(seq)),"dynamic", "gpa_analysis", "explanation"),
                self.create_text(" enrolled semesters, ", "template", None, "explanation"),
                self.create_text(self.pronoun_2.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" GPAs were ", "template", None, "explanation"),
                self.create_text(comma_sep_seq,"dynamic", "gpa_analysis", "explanation"),
                self.create_text(" respectively. ", "template", None, "explanation")
            ]

        return gpa_outliers_text

    def get_sig_gpa_inc_dec_text(self):
        #         GPA_INC_THRESHOLD = 0.3
        #         GPA_DEC_THRESHOLD = -0.3
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        sig_gpa_inc_dec_text = [self.create_text("", "template", None, "explanation")]
        sig_gpa_inc_dec_series = self.sem_df['gpa']
        connectors = ['Then', 'Afterward', 'Later',
                      'Then', 'Also', 'Later', 'Then']
        deltas = sig_gpa_inc_dec_series.diff()
        clauses = defaultdict(int)
        for ind, delta in enumerate(deltas):
            if delta > self.GPA_INC_THRESHOLD:
                clauses[ind + 1] = "increased " + str(round(delta, 1)) + " point(s), from " + \
                                   str(round(sig_gpa_inc_dec_series[ind], 1)) + " to " + str(
                    round(sig_gpa_inc_dec_series[ind + 1], 1))
            if delta < self.GPA_DEC_THRESHOLD:
                clauses[ind + 1] = "decreased " + str(abs(round(delta, 1))) + " point(s), from " + \
                                   str(round(sig_gpa_inc_dec_series[ind], 1)) + " to " + str(
                    round(sig_gpa_inc_dec_series[ind + 1], 1))
        if len(clauses) > 0:
            sig_gpa_inc_dec_text = [
                self.create_text(" Regarding ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text("\'s GPA, ", "template", None, "explanation")
            ]
            last_key = list(clauses.keys())[-1]
            for index, (sem_num, clause) in enumerate(clauses.items()):
                sig_gpa_inc_dec_text.append(self.create_text("in ", "template", None, "explanation"))
                sig_gpa_inc_dec_text.append(self.create_text(self.pronoun_2, "template", None, "explanation"))
                sig_gpa_inc_dec_text.append(self.create_text(" ", "template", None, "explanation"))
                sig_gpa_inc_dec_text.append(self.create_text(str(sem_num) + suffix(sem_num),"dynamic", "academic_period", "explanation"))
                sig_gpa_inc_dec_text.append(self.create_text(" semester, in ", "template", None, "explanation"))
                sig_gpa_inc_dec_text.append(self.create_text(self.sem_df.loc[sem_num]['academic_period'],"dynamic", "academic_period", "explanation"))
                sig_gpa_inc_dec_text.append(self.create_text(", it has significantly ", "template", None, "explanation"))
                sig_gpa_inc_dec_text.append(self.create_text(clause,"dynamic", "gpa", "explanation"))
                sig_gpa_inc_dec_text.append(self.create_text(". ", "template", None, "explanation"))

                if sem_num != last_key:
                    sig_gpa_inc_dec_text.append(self.create_text(connectors[index] + ", ", "template", None, "explanation"))

        return sig_gpa_inc_dec_text

    def get_sig_attempt_inc_dec_text(self):
        #         ATTEMPT_INC_THRESHOLD = 3
        #         ATTEMPT_DEC_THRESHOLD = -3
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        sig_attempt_inc_dec_text = [self.create_text("", "template", None, "explanation")]
        sig_attempt_inc_dec_series = self.sem_df['attempted_count']
        connectors = ['Then', 'Afterward', 'Later','Then', 'Also', 'Later', 'Then']
        deltas = sig_attempt_inc_dec_series.diff()
        clauses = defaultdict(int)
        for ind, delta in enumerate(deltas):
            if delta > self.ATTEMPT_INC_THRESHOLD:
                clauses[ind + 1] = "increased " + str(delta) + " credit hours, from " + \
                                   str(sig_attempt_inc_dec_series[ind]) + " to " + str(
                    sig_attempt_inc_dec_series[ind + 1]) + " credit hours"
            if delta < self.ATTEMPT_DEC_THRESHOLD:
                clauses[ind + 1] = "decreased " + str(abs(delta)) + " credit hours, from " + \
                                   str(sig_attempt_inc_dec_series[ind]) + " to " + str(
                    sig_attempt_inc_dec_series[ind + 1]) + " credit hours"
        if len(clauses) > 0:
            sig_attempt_inc_dec_text = [
                self.create_text(" Regarding ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text("\'s number of attempted credits, ", "template", None, "explanation")
            ]
            last_key = list(clauses.keys())[-1]
            for index, (sem_num, clause) in enumerate(clauses.items()):
                sig_attempt_inc_dec_text.append(self.create_text("in ", "template", None, "explanation"))
                sig_attempt_inc_dec_text.append(self.create_text(self.pronoun_2, "template", None, "explanation"))
                sig_attempt_inc_dec_text.append(self.create_text(" ", "template", None, "explanation"))
                sig_attempt_inc_dec_text.append(self.create_text(str(sem_num) + suffix(sem_num),"dynamic", "academic_period", "explanation"))
                sig_attempt_inc_dec_text.append(self.create_text(" semester, in ", "template", None, "explanation"))
                sig_attempt_inc_dec_text.append(self.create_text(self.sem_df.loc[sem_num]['academic_period'],"dynamic", "academic_period", "explanation"))
                sig_attempt_inc_dec_text.append(self.create_text(", it has significantly ", "template", None, "explanation"))
                sig_attempt_inc_dec_text.append(self.create_text(clause,"dynamic", "attempted_credits", "explanation"))
                sig_attempt_inc_dec_text.append(self.create_text(". ", "template", None, "explanation"))

                if sem_num != last_key:
                    sig_attempt_inc_dec_text.append(self.create_text(connectors[index] + ", ", "template", None, "explanation"))

        return sig_attempt_inc_dec_text

    def get_sig_withdrawn_inc_dec_text(self):
        #         WITHDRAWN_INC_THRESHOLD = 3
        #         WITHDRAWN_DEC_THRESHOLD = -3
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        sig_withdrawn_inc_dec_text = [self.create_text("", "template", None, "explanation")]
        sig_withdrawn_inc_dec_series = self.sem_df['withdrawn_count']
        connectors = ['Then', 'Afterward', 'Later',
                      'Then', 'Also', 'Later', 'Then']
        deltas = sig_withdrawn_inc_dec_series.diff()
        clauses = defaultdict(int)
        for ind, delta in enumerate(deltas):
            if delta > self.WITHDRAWN_INC_THRESHOLD:
                clauses[ind + 1] = "increased " + str(delta) + " credit hours, from " + \
                                   str(sig_withdrawn_inc_dec_series[ind]) + " to " + str(
                    sig_withdrawn_inc_dec_series[ind + 1]) + " credit hours"
            if delta < self.WITHDRAWN_DEC_THRESHOLD:
                clauses[ind + 1] = "decreased " + str(abs(delta)) + " credit hours, from " + \
                                   str(sig_withdrawn_inc_dec_series[ind]) + " to " + str(
                    sig_withdrawn_inc_dec_series[ind + 1]) + " credit hours"
        if len(clauses) > 0:
            sig_withdrawn_inc_dec_text = [
                self.create_text(" Regarding ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text("\'s number of withdrawn credits, ", "template", None, "explanation")
            ]
            last_key = list(clauses.keys())[-1]
            for index, (sem_num, clause) in enumerate(clauses.items()):
                sig_withdrawn_inc_dec_text.append(self.create_text("in ", "template", None, "explanation"))
                sig_withdrawn_inc_dec_text.append(self.create_text(self.pronoun_2, "template", None, "explanation"))
                sig_withdrawn_inc_dec_text.append(self.create_text(" ", "template", None, "explanation"))
                sig_withdrawn_inc_dec_text.append(self.create_text(str(sem_num) + suffix(sem_num),"dynamic", "academic_period", "explanation"))
                sig_withdrawn_inc_dec_text.append(self.create_text(" semester, in ", "template", None, "explanation"))
                sig_withdrawn_inc_dec_text.append(self.create_text(self.sem_df.loc[sem_num]['academic_period'],"dynamic", "academic_period", "explanation"))
                sig_withdrawn_inc_dec_text.append(self.create_text(", it has significantly ", "template", None, "explanation"))
                sig_withdrawn_inc_dec_text.append(self.create_text(clause,"dynamic", "withdrawn_credits", "explanation"))
                sig_withdrawn_inc_dec_text.append(self.create_text(". ", "template", None, "explanation"))

                if sem_num != last_key:
                    sig_withdrawn_inc_dec_text.append(self.create_text(connectors[index] + ", ", "template", None, "explanation"))

        return sig_withdrawn_inc_dec_text

    def get_sig_pass_inc_dec_text(self):
        #         PASS_INC_THRESHOLD = 3
        #         PASS_DEC_THRESHOLD = -3
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        sig_pass_inc_dec_text = [self.create_text("", "template", None, "explanation")]
        sig_pass_inc_dec_series = self.sem_df['passed_count']
        connectors = ['Then', 'Afterward', 'Later',
                      'Then', 'Also', 'Later', 'Then']
        deltas = sig_pass_inc_dec_series.diff()
        clauses = defaultdict(int)
        for ind, delta in enumerate(deltas):
            if delta > self.PASS_INC_THRESHOLD:
                clauses[ind + 1] = "increased " + str(delta) + " credit hours, from " + \
                                   str(sig_pass_inc_dec_series[ind]) + " to " + str(
                    sig_pass_inc_dec_series[ind + 1]) + " credit hours"
            if delta < self.PASS_DEC_THRESHOLD:
                clauses[ind + 1] = "decreased " + str(abs(delta)) + " credit hours, from " + \
                                   str(sig_pass_inc_dec_series[ind]) + " to " + str(
                    sig_pass_inc_dec_series[ind + 1]) + " credit hours"
        if len(clauses) > 0:
            sig_pass_inc_dec_text = [
                self.create_text(" Regarding ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text("\'s number of passed credits, ", "template", None, "explanation")
            ]
            last_key = list(clauses.keys())[-1]
            for index, (sem_num, clause) in enumerate(clauses.items()):
                sig_pass_inc_dec_text.append(self.create_text("in ", "template", None, "explanation"))
                sig_pass_inc_dec_text.append(self.create_text(self.pronoun_2, "template", None, "explanation"))
                sig_pass_inc_dec_text.append(self.create_text(" ", "template", None, "explanation"))
                sig_pass_inc_dec_text.append(self.create_text(str(sem_num) + suffix(sem_num),"dynamic", "academic_period", "explanation"))
                sig_pass_inc_dec_text.append(self.create_text(" semester, in ", "template", None, "explanation"))
                sig_pass_inc_dec_text.append(self.create_text(self.sem_df.loc[sem_num]['academic_period'],"dynamic", "academic_period", "explanation"))
                sig_pass_inc_dec_text.append(self.create_text(", it has significantly ", "template", None, "explanation"))
                sig_pass_inc_dec_text.append(self.create_text(clause,"dynamic", "passed_credits", "explanation"))
                sig_pass_inc_dec_text.append(self.create_text(". ", "template", None, "explanation"))

                if sem_num != last_key:
                    sig_pass_inc_dec_text.append(self.create_text(connectors[index] + ", ", "template", None, "explanation"))

        return sig_pass_inc_dec_text

    def get_sig_fail_inc_dec_text(self):
        #         FAIL_INC_THRESHOLD = 3
        #         FAIL_DEC_THRESHOLD = -3
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        sig_fail_inc_dec_text = [self.create_text("", "template", None, "explanation")]
        sig_fail_inc_dec_series = self.sem_df['failed_count']
        connectors = ['Then', 'Afterward', 'Later',
                      'Then', 'Also', 'Later', 'Then']
        deltas = sig_fail_inc_dec_series.diff()
        clauses = defaultdict(int)
        for ind, delta in enumerate(deltas):
            if delta > self.FAIL_INC_THRESHOLD:
                clauses[ind + 1] = "increased " + str(delta) + " credit hours, from " + \
                                   str(sig_fail_inc_dec_series[ind]) + " to " + str(
                    sig_fail_inc_dec_series[ind + 1]) + " credit hours"
            if delta < self.FAIL_DEC_THRESHOLD:
                clauses[ind + 1] = "decreased " + str(abs(delta)) + " credit hours, from " + \
                                   str(sig_fail_inc_dec_series[ind]) + " to " + str(
                    sig_fail_inc_dec_series[ind + 1]) + " credit hours"
        if len(clauses) > 0:
            sig_fail_inc_dec_text = [
                self.create_text(" Regarding ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text("\'s number of failed credits, ", "template", None, "explanation")
            ]
            last_key = list(clauses.keys())[-1]
            for index, (sem_num, clause) in enumerate(clauses.items()):
                sig_fail_inc_dec_text.append(self.create_text("in ", "template", None, "explanation"))
                sig_fail_inc_dec_text.append(self.create_text(self.pronoun_2, "template", None, "explanation"))
                sig_fail_inc_dec_text.append(self.create_text(" ", "template", None, "explanation"))
                sig_fail_inc_dec_text.append(self.create_text(str(sem_num) + suffix(sem_num),"dynamic", "academic_period", "explanation"))
                sig_fail_inc_dec_text.append(self.create_text(" semester, in ", "template", None, "explanation"))
                sig_fail_inc_dec_text.append(self.create_text(self.sem_df.loc[sem_num]['academic_period'],"dynamic", "academic_period", "explanation"))
                sig_fail_inc_dec_text.append(self.create_text(", it has significantly ", "template", None, "explanation"))
                sig_fail_inc_dec_text.append(self.create_text(clause,"dynamic", "failed_credits", "explanation"))
                sig_fail_inc_dec_text.append(self.create_text(". ", "template", None, "explanation"))

                if sem_num != last_key:
                    sig_fail_inc_dec_text.append(self.create_text(connectors[index] + ", ", "template", None, "explanation"))

        return sig_fail_inc_dec_text

    def get_sig_d_scored_inc_dec_text(self):
        #         D_SCORED_INC_THRESHOLD = 3
        #         D_SCORED_DEC_THRESHOLD = -3
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        sig_d_scored_inc_dec_text = [self.create_text("", "template", None, "explanation")]
        sig_d_scored_inc_dec_series = self.sem_df['d_scored_count']
        connectors = ['Then', 'Afterward', 'Later',
                      'Then', 'Also', 'Later', 'Then']
        deltas = sig_d_scored_inc_dec_series.diff()
        clauses = defaultdict(int)
        for ind, delta in enumerate(deltas):
            if delta > self.D_SCORED_INC_THRESHOLD:
                clauses[ind + 1] = "increased " + str(delta) + " credit hours, from " + \
                                   str(sig_d_scored_inc_dec_series[ind]) + " to " + str(
                    sig_d_scored_inc_dec_series[ind + 1]) + " credit hours"
            if delta < self.D_SCORED_DEC_THRESHOLD:
                clauses[ind + 1] = "decreased " + str(abs(delta)) + " credit hours, from " + \
                                   str(sig_d_scored_inc_dec_series[ind]) + " to " + str(
                    sig_d_scored_inc_dec_series[ind + 1]) + " credit hours"
        if len(clauses) > 0:
            sig_d_scored_inc_dec_text = [
                self.create_text(" Regarding ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "student_name", "explanation"),
                self.create_text("\'s number of credits with D score, ", "template", None, "explanation")
            ]
            last_key = list(clauses.keys())[-1]
            for index, (sem_num, clause) in enumerate(clauses.items()):
                sig_d_scored_inc_dec_text.append(self.create_text("in ", "template", None, "explanation"))
                sig_d_scored_inc_dec_text.append(self.create_text(self.pronoun_2, "template", None, "explanation"))
                sig_d_scored_inc_dec_text.append(self.create_text(" ", "template", None, "explanation"))
                sig_d_scored_inc_dec_text.append(self.create_text(str(sem_num) + suffix(sem_num),"dynamic", "academic_period", "explanation"))
                sig_d_scored_inc_dec_text.append(self.create_text(" semester, in ", "template", None, "explanation"))
                sig_d_scored_inc_dec_text.append(self.create_text(self.sem_df.loc[sem_num]['academic_period'],"dynamic", "academic_period", "explanation"))
                sig_d_scored_inc_dec_text.append(self.create_text(", it has significantly ", "template", None, "explanation"))
                sig_d_scored_inc_dec_text.append(self.create_text(clause,"dynamic", "d_scored_credits", "explanation"))
                sig_d_scored_inc_dec_text.append(self.create_text(". ", "template", None, "explanation"))

                if sem_num != last_key:
                    sig_d_scored_inc_dec_text.append(self.create_text(connectors[index] + ", ", "template", None, "explanation"))

        return sig_d_scored_inc_dec_text

    def get_semester_events(self):
        COLUMN_NAMES = [
            'academic_period',
            'is_summer',
            'attempted_count',
            'passed_count',
            'failed_count',
            'withdrawn_count',
            'd_scored_count',
            'transferred_count',
            'gpa',
            'attempted_courses',
            'passed_courses',
            'failed_courses',
            'withdrawn_courses',
            'd_scored_courses',
            'transferred_courses',
            'academic_standing',
            'cgpa',
            'major',
            'advisor_count',
            'expected_graduation_date'
        ]
        sem_df = pd.DataFrame(columns=COLUMN_NAMES)
        sem_with_summers_df = pd.DataFrame(columns=COLUMN_NAMES)

        sem_academic_period = []
        sem_gpa = []

        course_work = defaultdict(list)
        core_course_work = defaultdict(list)
        lowest_grade = ''
        # Summer semesters count
        summer_semesters_set = set()
        semesters_names = set()
        summer_semesters_count = 0
        # Outcome found!
        found_outcome = (False if self.data['outcome'] is None else True)
        # Attempted credits
        attempted_credits = 0.0

        # Passed credits
        passed_credits_count = 0.0
        passed_credits = set()
        # Withdrawn credits
        withdrawn_credits_count = 0.0
        withdrawn_credits = set()
        # Failed credits
        failed_credits_count = 0.0
        failed_credits = set()
        # D scored credits
        d_credits_count = 0.0
        d_credits = set()
        # Transferred credits
        transferred_courses_count = 0.0
        transferred_courses = set()

        # Academic standing
        academic_standing = []
        good_standing_sem_count = 0
        probation_sem_count = 0
        suspended_academic_count = 0
        # Advisor count
        advisor_count = 0.0

        for index, sem in enumerate(self.data['semesters'], 1):
            try:
                if sem['semesterInfo']['advisor_count'] > advisor_count:
                    advisor_count = sem['semesterInfo']['advisor_count']
            except:
                pass
            # Getting academic standings
            try:
                academic_standing.append(sem['semesterInfo']['academic_standing_desc'])
            except:
                pass
            # This line for finding number of summer semesters
            semesters_names.add(sem['courses'][0]['academic_period_desc'])
            if 'summer' in sem['courses'][0]['academic_period_desc'].lower():
                summer_semesters_set.add(
                    sem['courses'][0]['academic_period_desc'])

            #           semester based events
            sem_attempted_count = 0
            sem_passed_count = 0
            sem_failed_count = 0
            sem_withdrawn_count = 0
            sem_attempted_courses = []
            sem_passed_courses = []
            sem_failed_courses = []
            sem_withdrawn_courses = []

            sem_d_scored_count = 0
            sem_transferred_count = 0
            sem_d_scored_courses = []
            sem_transferred_courses = []

            sem_with_summers_attempted_count = 0
            sem_with_summers_passed_count = 0
            sem_with_summers_failed_count = 0
            sem_with_summers_withdrawn_count = 0
            sem_with_summers_attempted_courses = []
            sem_with_summers_passed_courses = []
            sem_with_summers_failed_courses = []
            sem_with_summers_withdrawn_courses = []

            sem_with_summers_d_scored_count = 0
            sem_with_summers_transferred_count = 0
            sem_with_summers_d_scored_courses = []
            sem_with_summers_transferred_courses = []

            #             if 'Summer' not in sem['semesterInfo']['academic_period_desc']:
            for course in sem['courses']:
                course_work[course['course_title_short']].append((course['academic_period_desc'], course['final_grade']))
                # Getting core courses work
                if course['course_identification'] in ["ITCS1212", "ITSC1212", "ITCS1213", "ITSC1213", "ITCS2214",
                                                       "ITSC2214", "ITCS2175", "ITSC2175"]:
                    core_course_work[course['course_identification']].append((course['academic_period_desc'], course['final_grade']))

                if course['transfer_course_ind'] == "N" and course['final_grade'] in ['A', 'B', 'C', 'D', 'F']:
                    if course['final_grade'] > lowest_grade:
                        lowest_grade = course['final_grade']
                # Getting attempted credits

                if course['transfer_course_ind'] == 'N':
                    if not math.isnan(course['credits_attempted']):
                        attempted_credits = attempted_credits + \
                            course['credits_attempted']
                        sem_with_summers_attempted_count = sem_with_summers_attempted_count + \
                            course['credits_attempted']
                        sem_with_summers_attempted_courses.append(course['course_title_short'])
                        if 'Summer' not in sem['semesterInfo']['academic_period_desc']:
                            sem_attempted_count = sem_attempted_count + \
                                course['credits_attempted']
                            sem_attempted_courses.append(course['course_title_short'])

                # Getting passed credits and count

                if course['transfer_course_ind'] == 'N':
                    if not math.isnan(course['credits_passed']):
                        passed_credits_count = passed_credits_count + \
                            course['credits_passed']
                        passed_credits.add(
                            course['course_title_short'].title())
                        sem_with_summers_passed_count = sem_with_summers_passed_count + \
                            course['credits_passed']
                        if course['credits_passed'] > 0:
                            sem_with_summers_passed_courses.append(course['course_title_short'])
                        if 'Summer' not in sem['semesterInfo']['academic_period_desc']:
                            sem_passed_count = sem_passed_count + \
                                course['credits_passed']
                            if course['credits_passed'] > 0:
                                sem_passed_courses.append(course['course_title_short'])
                # Getting withdrawn credits and count
                if course['transfer_course_ind'] == 'N' and course['final_grade'] == 'W':
                    withdrawn_credits_count = withdrawn_credits_count + \
                        course['credits_attempted']
                    withdrawn_credits.add(course['course_title_short'].title())
                    sem_with_summers_withdrawn_count = sem_with_summers_withdrawn_count + \
                        course['credits_attempted']
                    sem_with_summers_withdrawn_courses.append(course['course_title_short'])
                    if 'Summer' not in sem['semesterInfo']['academic_period_desc']:
                        sem_withdrawn_count = sem_withdrawn_count + \
                            course['credits_attempted']
                        sem_withdrawn_courses.append(course['course_title_short'])
                # Getting failed credits and count
                if course['course_failed_ind'] == "Y" and course['transfer_course_ind'] == "N":
                    if not math.isnan(course['credits_attempted']):
                        failed_credits_count = failed_credits_count + \
                            course['credits_attempted']
                        failed_credits.add(course['course_title_short'].title())
                        sem_with_summers_failed_count = sem_with_summers_failed_count + \
                            course['credits_attempted']
                        sem_with_summers_failed_courses.append(course['course_title_short'])
                        if 'Summer' not in sem['semesterInfo']['academic_period_desc']:
                            sem_failed_count = sem_failed_count + \
                                course['credits_attempted']
                            sem_failed_courses.append(course['course_title_short'])
                # Getting D-scored credits
                if course['transfer_course_ind'] == 'N' and course['final_grade'] == 'D':
                    d_credits_count = d_credits_count + \
                        course['credits_attempted']
                    d_credits.add(course['course_title_short'].title())
                    sem_with_summers_d_scored_count = sem_with_summers_d_scored_count + \
                        course['credits_attempted']
                    sem_with_summers_d_scored_courses.append(course['course_title_short'])
                    if 'Summer' not in sem['semesterInfo']['academic_period_desc']:
                        sem_d_scored_count = sem_d_scored_count + \
                            course['credits_attempted']
                        sem_d_scored_courses.append(course['course_title_short'])
                # Getting transferred credits and count
                if course['transfer_course_ind'] == "Y":
                    if not math.isnan(course['credits_attempted']):
                        transferred_courses_count = transferred_courses_count + \
                            course['credits_attempted']
                        sem_with_summers_transferred_count = sem_with_summers_transferred_count + course[
                            'credits_attempted']
                        try:
                            transferred_courses.add(course['course_title_short'].title())
                            sem_with_summers_transferred_courses.append(course['course_title_short'].title())
                        except Exception as e:
                            pass
                    if 'Summer' not in sem['semesterInfo']['academic_period_desc']:
                        sem_transferred_count = sem_transferred_count + \
                            course['credits_attempted']
                        try:
                            sem_transferred_courses.append(course['course_title_short'].title())
                        except Exception as e:
                            pass

            is_summer = 'yes' if 'Summer' in sem['semesterInfo']['academic_period_desc'] else 'no'
            if 'Summer' not in sem['semesterInfo']['academic_period_desc']:
                sem_df = sem_df.append({
                    'academic_period': sem['semesterInfo']['academic_period_desc'],
                    'is_summer': is_summer,
                    'attempted_count': int(sem_attempted_count),
                    'passed_count': int(sem_passed_count),
                    'failed_count': int(sem_failed_count),
                    'withdrawn_count': int(sem_withdrawn_count),
                    'd_scored_count': int(sem_d_scored_count),
                    'transferred_count': int(sem_transferred_count),
                    'gpa': round(sem['semesterInfo']['gpa'], 1),
                    'attempted_courses': ', '.join(item for item in sem_attempted_courses),
                    'passed_courses': ', '.join(item for item in sem_passed_courses),
                    'failed_courses': ', '.join(item for item in sem_failed_courses),
                    'withdrawn_courses': ', '.join(item for item in sem_withdrawn_courses),
                    'd_scored_courses': ', '.join(item for item in sem_d_scored_courses),
                    'transferred_courses': ', '.join(item for item in sem_transferred_courses),
                    'academic_standing': sem['semesterInfo']['academic_standing_desc'],
                    'cgpa': round(sem['semesterInfo']['CGPA'], 1),
                    'major': sem['semesterInfo']['major_desc'],
                    'advisor_count': sem['semesterInfo']['advisor_count'],
                    'expected_graduation_date': sem['semesterInfo']['expected_graduation_date']
                }, ignore_index=True)
                sem_df.index += 1

            sem_with_summers_df = sem_with_summers_df.append({
                'academic_period': sem['semesterInfo']['academic_period_desc'],
                'is_summer': is_summer,
                'attempted_count': int(sem_with_summers_attempted_count),
                'passed_count': int(sem_with_summers_passed_count),
                'failed_count': int(sem_with_summers_failed_count),
                'withdrawn_count': int(sem_with_summers_withdrawn_count),
                'd_scored_count': int(sem_with_summers_d_scored_count),
                'transferred_count': int(sem_with_summers_transferred_count),
                'gpa': round(sem['semesterInfo']['gpa'], 1),
                'attempted_courses': ', '.join(item for item in sem_with_summers_attempted_courses),
                'passed_courses': ', '.join(item for item in sem_with_summers_passed_courses),
                'failed_courses': ', '.join(item for item in sem_with_summers_failed_courses),
                'withdrawn_courses': ', '.join(item for item in sem_with_summers_withdrawn_courses),
                'd_scored_courses': ', '.join(item for item in sem_with_summers_d_scored_courses),
                'transferred_courses': ', '.join(item for item in sem_with_summers_transferred_courses),
                'academic_standing': sem['semesterInfo']['academic_standing_desc'],
                'cgpa': round(sem['semesterInfo']['CGPA'], 1),
                'major': sem['semesterInfo']['major_desc'],
                'advisor_count': sem['semesterInfo']['advisor_count'],
                'expected_graduation_date': sem['semesterInfo']['expected_graduation_date']
            }, ignore_index=True)
            sem_with_summers_df.index += 1

        return sem_df, sem_with_summers_df, course_work, core_course_work, lowest_grade

    def get_withdrawn_then_passed(self):
        for course, grade_list in self.course_work.items():
            if len(grade_list) > 1:
                if grade_list[0][1] == 'W' and grade_list[1][1] == 'A':
                    return (course, grade_list[0][0], 'an ' + grade_list[1][1], grade_list[1][0])
                elif grade_list[0][1] == 'W' and grade_list[1][1] == 'B':
                    return (course, grade_list[0][0], 'a ' + grade_list[1][1], grade_list[1][0])
        return ('', '', '', '')

    def get_failed_then_passed(self):
        for course, grade_list in self.course_work.items():
            if len(grade_list) > 1:
                if grade_list[0][1] == 'F' and grade_list[1][1] == 'A':
                    return (course, grade_list[0][0], 'an ' + grade_list[1][1], grade_list[1][0])
                elif grade_list[0][1] == 'F' and grade_list[1][1] == 'B':
                    return (course, grade_list[0][0], 'a ' + grade_list[1][1], grade_list[1][0])
        return ('', '', '', '')

    def get_demographic_data(self):
        temp_dict = self.data['background']['demographics']
        age_admitted = 0
        try:
            if type(self.data['semesters'][0]['semesterInfo']['age_admitted']) == str:
                age_admitted = self.data['semesters'][0]['semesterInfo']['age_admitted'].replace(".00", "")
            age_admitted = int(self.data['semesters'][0]['semesterInfo']['age_admitted'])
        except:
            pass
        primary_ethnicity = (temp_dict['primary_ethnicity_desc'].lower() if type(temp_dict['primary_ethnicity_desc']) == str and len(temp_dict['primary_ethnicity_desc']) > 2 else '')
        if primary_ethnicity == 'other': 
            primary_ethnicity = ''
        gender = temp_dict['gender_desc'].lower()
        current_age = int(self.data["background"]["demographics"]['current_age'])
        return (self.p.number_to_words(int(age_admitted)), primary_ethnicity, gender, current_age)

    def get_pronouns(self):
        return (("He", "his", "him") if self.data['background']['demographics']['gender_desc'] == "Male" else (  "She", "her", "her"))

    def get_major(self):
        return self.data['semesters'][0]['semesterInfo']['major_desc']

    def get_admission_population(self):
        try:
            if 'Freshmen' in self.data['semesters'][0]['semesterInfo']['admissions_population_desc']:
                return 'freshman'
            elif 'Transfer' in self.data['semesters'][0]['semesterInfo']['admissions_population_desc']:
                return 'transfer'
            else:
                return ''
        except:
            return ''

    def get_enrollment_date(self):
        return self.data['semesters'][0]['courses'][0]['academic_period_desc']

    def get_expected_grad(self):
        today = date.today()
        current_year = today.year

        semester_names = {
            '12': "Spring ",
            '5': "First Summer ",
            '05': "First Summer ",
            '6': "Second Summer ",
            '06': "Second Summer ",
            '8': "Fall ",
            '08': "Fall "
        }

        try:
            temp_date = self.data['semesters'][-1]['semesterInfo']['expected_graduation_date'].split('/')

            grad_year = temp_date[0]
            grad_month = temp_date[1]
            grad_day = temp_date[2]

            grad_date = date(int(grad_year), int(grad_month), int(grad_day))

            if grad_date > today:
                return semester_names[grad_month] + grad_year, 'future'
            else:
                return semester_names[grad_month] + grad_year, 'past'

        except Exception as e:
            return "", ""

    def get_graduation_status(self):
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        def custom_strftime(format, t):
            return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

        def get_date(date):
            date = str(date)
            semester_names = {
                1: "Spring ",
                5: "First Summer ",
                6: "First Summer ",
                7: "Second Summer ",
                8: "Fall "
            }
            return semester_names[int(date[4:5])] + str(date[:4])

        if self.data['grad_info']:
            if self.data['grad_info']['isGraduated'] == "Yes":
                return (True, get_date(self.data['grad_info']['last_semester_enrolled']),
                        get_date(self.data['grad_info']['last_semester_enrolled']))
            elif self.data['grad_info']['isGraduated'] == "No":
                return (False, '', get_date(self.data['grad_info']['last_semester_enrolled']))

        elif self.data['outcome']:
            date = self.data['outcome']['outcome_graduation_date']
            if len(date) > 9:
                year = int(date[:4])
                month = int(date[5:7])
                day = int(date[8:11])
            return (True, semester_names[month] + str(year), '')

        else:
            return (False, '', '')

    def get_gpa(self):
        if self.data['outcome'] is None:
            return (False, 0)
        else:
            return (True, round(self.data['latest_CGPA'], 1))

    def get_course_level(self):
        grad_level_count = 0.0
        u_grad_level_count = 0.0
        grad_level_courses = set()
        u_grad_level_courses = set()
        for k, v in self.semesters_list.items():
            for item in v:
                if item['transfer_course_ind'] == "N" and item['course_level_desc'] == "Graduate":
                    grad_level_count = grad_level_count + \
                        item['credits_attempted']
                    grad_level_courses.add(item['course_identification'])
                elif item['transfer_course_ind'] == "N" and item['course_level_desc'] == "Undergraduate":
                    u_grad_level_count = u_grad_level_count + \
                        item['credits_attempted']
                    u_grad_level_courses.add(item['course_identification'])
        return (int(grad_level_count), int(u_grad_level_count), grad_level_courses, u_grad_level_courses)

    def major_change(self):
        def suffix(d):
            return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

        start_major_index = next(iter(sorted(self.data["semesters"]["academic_study"])))
        for item in self.data["semesters"]["academic_study"][start_major_index]:
            start_major = item["major_desc"]
            break
        for k, v in iter(sorted(self.data["semesters"]["academic_study"].items())):
            for item2 in v:
                if item2["major_desc"] != start_major:
                    return str(self.data["background"]["demographics"]["person_uid"]) + ": CHANGED MAJOR TO " + item2[
                        "major_desc"] + " FROM " + start_major + " in his/her " + str(k) + suffix(int(k)) + " semester"

    def create_text(self, text, tag, feature, explanation):
        return {
            "text": text,
            "tag": tag,
            "feature": feature,
            "explanation": explanation
        }

    def get_significant_failed(self):
        sig_failed_text = [self.create_text("", "template", None, "explanation")]
        sig_failed_vector = self.sem_df['failed_count']
        delta_vector = sig_failed_vector.diff()

    def get_dem_text(self):
        dem_text = [self.create_text("", "template", None, "explanation")]
        if self.age_admitted != 'zero':
            dem_text = [
                self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                self.create_text(" is a ", "template", None, "explanation"),
                self.create_text(self.gender,"dynamic", "gender", "explanation"),
                self.create_text(" student who was admitted at the age of ", "template", None, "explanation"),
                self.create_text(self.age_admitted,"dynamic", "age_admitted", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
                self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                self.create_text(" was first enrolled in ", "template", None, "explanation"),
                self.create_text(self.enrollment_date,"dynamic", "enrollment_date", "explanation"),
                self.create_text(" and started with a major in ", "template", None, "explanation"),
                self.create_text(self.major,"dynamic", "major", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]
        else:
            dem_text = [
                self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                self.create_text(" is a ", "template", None, "explanation"),
                self.create_text(self.gender,"dynamic", "gender", "explanation"),
                self.create_text(" student who was first enrolled in ", "template", None, "explanation"),
                self.create_text(self.enrollment_date,"dynamic", "enrollment_date", "explanation"),
                self.create_text(" and started with a major in ", "template", None, "explanation"),
                self.create_text(self.major,"dynamic", "major", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]
        return dem_text

    def get_specific_dem_text(self):  # if admission_population in args
        specific_dem_text = [self.create_text("", "template", None, "explanation")]
        if 'Yes' in [self.choices['Admissions population']]:
            if self.admission_population != "" and self.age_admitted != 'zero':
                specific_dem_text = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" ", "template", None, "explanation"),
                    self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.gender,"dynamic", "gender", "explanation"),
                    self.create_text(" student who was admitted as a ", "template", None, "explanation"),
                    self.create_text(self.admission_population,"dynamic", "admissions_population_desc", "explanation"),
                    self.create_text(" student at the age of ", "template", None, "explanation"),
                    self.create_text(self.age_admitted,"dynamic", "age_admitted", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                    self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                    self.create_text(" was first enrolled in ", "template", None, "explanation"),
                    self.create_text(self.enrollment_date,"dynamic", "enrollment_date", "explanation"),
                    self.create_text(" and started with a major in ", "template", None, "explanation"),
                    self.create_text(self.major,"dynamic", "major", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            ###############################################################################################
            elif self.age_admitted != 'zero':
                specific_dem_text = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" ", "template", None, "explanation"),
                    self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.gender,"dynamic", "gender", "explanation"),
                    self.create_text(" student who was admitted at the age of ", "template", None, "explanation"),
                    self.create_text(self.age_admitted,"dynamic", "age_admitted", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                    self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                    self.create_text(" was first enrolled in ", "template", None, "explanation"),
                    self.create_text(self.enrollment_date,"dynamic", "enrollment_date", "explanation"),
                    self.create_text(" and started with a major in ", "template", None, "explanation"),
                    self.create_text(self.major,"dynamic", "major", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
        else:
            specific_dem_text = [
                self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                self.create_text(" ", "template", None, "explanation"),
                self.create_text(self.last_name,"dynamic", "last_name", "explanation"),
                self.create_text(" is a ", "template", None, "explanation"),
                self.create_text(self.gender,"dynamic", "gender", "explanation"),
                self.create_text(" student who was first enrolled in ", "template", None, "explanation"),
                self.create_text(self.enrollment_date,"dynamic", "enrollment_date", "explanation"),
                self.create_text(" and started with a major in ", "template", None, "explanation"),
                self.create_text(self.major,"dynamic", "major", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]

        additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 0001
        if self.choices['Citizenship type'] == "No" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "Yes":
            if self.primary_ethnicity != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "No" and self.choices['Current age'] == "Yes" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "No":
            if self.current_age != "":
                additional_dem_info = [
                    self.create_text("Currently, ", "template", None, "explanation"),
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "No" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "No":
            if self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text("\'s nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 1000
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "No":
            if self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.citizenship_desc[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "Yes":
            if self.primary_ethnicity != "" and self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "Yes" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "No":
            if self.citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.citizenship_desc[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old now. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is now ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 1100
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "No":
            if self.citizenship_desc != "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" \'s nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "No" and self.choices['Current age'] == "Yes" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "No":
            if self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text("\'s nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" and ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old now. ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old now. ", "template", None, "explanation"),
                ]
            elif self.current_age == "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text("\'s nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]

        # 1101
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "Yes":
            if self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc == "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(" and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text("student. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" \'s nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 1110
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "Yes" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "No":
            if self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),

                ]
            elif self.citizenship_desc == "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" \'s nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),

                ]
            elif self.citizenship_desc != "" and self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and currently ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),

                ]
            elif self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" \'s nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old now. ", "template", None, "explanation"),

                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "Yes" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "Yes":
            if self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc == "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(" student and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and currently ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc == "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text("\'s nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and currently ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc == "" and self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(" student and currently ", "template", None, "explanation"),
                    self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc == "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(" student. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text("\'s  nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.current_age != "":
                additional_dem_info = [
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        
        specific_dem_text = specific_dem_text + additional_dem_info
        if all(item == 'No' for item in list(self.choices.values())[0:6]):
            specific_dem_text = self.dem_text
        return specific_dem_text

    def get_specific_intro_text(self):  # if admission_population in args
        specific_intro_text = [self.create_text("", "template", None, "explanation")]
        if 'Yes' in [self.choices['Admissions population']]:
            if self.admission_population != "" and self.age_admitted != 'zero':
                specific_intro_text = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" was admitted as a ", "template", None, "explanation"),
                    self.create_text(self.admission_population,"dynamic", "admissions_population_desc", "explanation"),
                    self.create_text(" student at the age of ", "template", None, "explanation"),
                    self.create_text(self.age_admitted,"dynamic", "age_admitted", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" was first enrolled in ", "template", None, "explanation"),
                    self.create_text(self.enrollment_date,"dynamic", "enrollment_date", "explanation"),
                    self.create_text(" and started with a major in ", "template", None, "explanation"),
                    self.create_text(self.major,"dynamic", "major", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            ###############################################################################################
            elif self.age_admitted != 'zero':
                specific_intro_text = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" was admitted at the age of ", "template", None, "explanation"),
                    self.create_text(self.age_admitted,"dynamic", "age_admitted", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" was first enrolled in ", "template", None, "explanation"),
                    self.create_text(self.enrollment_date,"dynamic", "enrollment_date", "explanation"),
                    self.create_text(" and started with a major in ", "template", None, "explanation"),
                    self.create_text(self.major,"dynamic", "major", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
        else:
            specific_intro_text = [
                self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                self.create_text(" was first enrolled in ", "template", None, "explanation"),
                self.create_text(self.enrollment_date,"dynamic", "enrollment_date", "explanation"),
                self.create_text(" and started with a major in ", "template", None, "explanation"),
                self.create_text(self.major,"dynamic", "major", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]

        additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 0001
        if self.choices['Citizenship type'] == "No" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "Yes":
            if self.primary_ethnicity != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "No" and self.choices['Current age'] == "Yes" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "No":
            if self.current_age != "":
                additional_dem_info = [
                    self.create_text("Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "No" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "No": # 0100
            if self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 1000
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "No":
            if self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.citizenship_desc[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "No" and self.choices['Primary ethnicity'] == "Yes":  # 1001
            if self.primary_ethnicity != "" and self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == 'Yes' and self.choices['Nation of citizenship'] == 'No' and self.choices['Current age'] == 'Yes' and self.choices['Primary ethnicity'] == 'No':  # 1010
            if self.citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.citizenship_desc[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words( self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old now. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is now ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 1100
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "No":
            if self.citizenship_desc != "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 1101
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "No" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "Yes":
            if self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc == "" and self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(" and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text("student. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        # 1110
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "Yes" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "No":
            if self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc == "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),

                ]
            elif self.citizenship_desc != "" and self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and currently ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),

                ]
            elif self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old now. ", "template", None, "explanation"),

                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        elif self.choices['Citizenship type'] == "Yes" and self.choices['Current age'] == "Yes" and self.choices['Nation of citizenship'] == "Yes" and self.choices['Primary ethnicity'] == "Yes": # 1111
            if self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc == "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(" student and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and currently ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc == "" and self.nation_of_citizenship_desc != "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". Currently, ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and currently ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity == "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc == "" and self.nation_of_citizenship_desc == "" and self.current_age != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(" student and currently ", "template", None, "explanation"),
                    self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc != "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen and ", "template", None, "explanation"),
                    self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "" and self.citizenship_desc != "" and self.nation_of_citizenship_desc == "" and self.current_age == "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(", ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.primary_ethnicity != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is an ", "template", None, "explanation") if self.primary_ethnicity[0] in ['a', 'e', 'u', 'i', 'o'] else self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.primary_ethnicity.lower(),"dynamic", "primary_ethnicity", "explanation"),
                    self.create_text(" student. ", "template", None, "explanation"),
                ]
            elif self.citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" is a ", "template", None, "explanation"),
                    self.create_text(self.citizenship_desc.lower(),"dynamic", "citizenship_desc", "explanation"),
                    self.create_text(" citizen. ", "template", None, "explanation"),
                ]
            elif self.nation_of_citizenship_desc != "":
                additional_dem_info = [
                    self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" nation of citizenship in ", "template", None, "explanation"),
                    self.create_text(self.nation_of_citizenship_desc.title(),"dynamic", "nation_of_citizenship_desc", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
            elif self.current_age != "":
                additional_dem_info = [
                    self.create_text("Currently, ", "template", None, "explanation"),
                    self.create_text(self.first_name,"dynamic", "first_name", "explanation"),
                    self.create_text(" is ", "template", None, "explanation"),
                    self.create_text(self.p.number_to_words(self.current_age),"dynamic", "current_age", "explanation"),
                    self.create_text(" years old. ", "template", None, "explanation"),
                ]
            # else:
            #     additional_dem_info = [self.create_text("", 'template', None, "explanation")]
        specific_intro_text += additional_dem_info

        return specific_intro_text

    def get_trans_text(self):
        trans_text = [self.create_text("", "template", None, "explanation")]
        if self.transferred_courses_count > 0:
            trans_text = [
                self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                self.create_text(" transferred a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.transferred_courses_count),"dynamic", "transferred_credits", "explanation"),
                self.create_text(" credit hours from ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" previous school. ", "template", None, "explanation"),
            ]
        return trans_text

    def get_d_credits_text(self):
        d_credits_text = [self.create_text("", "template", None, "explanation")]
        if self.d_credits_count > 0:
            d_credits_text = [
                self.create_text("Besides, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" has scored D in a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.d_credits_count),"dynamic", "final_grade", "explanation"),
                self.create_text(" credit hours. ", "template", None, "explanation"),
            ]
        return d_credits_text

    def get_lowest_text(self):
        lowest_text = [self.create_text("", "template", None, "explanation")]
        if self.lowest_grade == '':
            return lowest_text
        elif self.lowest_grade == 'F' or self.lowest_grade == 'D':
            return lowest_text
        elif self.lowest_grade != 'A':
            lowest_text = [
                self.create_text("Throughout ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" enrollment in this major, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" maintained all ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" grades at ", "template", None, "explanation"),
                self.create_text(self.lowest_grade,"dynamic", "final_grade", "explanation"),
                self.create_text(" or above. ", "template", None, "explanation"),
            ]
        else:
            lowest_text = [
                self.create_text("Throughout ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" enrollment in this major, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" maintained all ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" grades at ", "template", None, "explanation"),
                self.create_text(self.lowest_grade,"dynamic", "final_grade", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]
        return lowest_text

    def get_failed_then_passed_text(self):
        failed_then_passed_text = [self.create_text("", "template", None, "explanation")]
        if self.failed_course != '':
            failed_then_passed_text = [
                self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                self.create_text(" failed the course ", "template", None, "explanation"),
                self.create_text(self.failed_course,"dynamic", "final_grade", "explanation"),
                self.create_text(" in ", "template", None, "explanation"),
                self.create_text(self.semester_failed_course,"dynamic", "academic_period_desc", "explanation"),
                self.create_text(" but achieved ", "template", None, "explanation"),
                self.create_text(self.new_grade_f,"dynamic", "final_grade", "explanation"),
                self.create_text(" retaking the same course in ", "template", None, "explanation"),
                self.create_text(self.semester_passed_course_f,"dynamic", "academic_period_desc", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]
        return failed_then_passed_text

    def get_grad_text(self):
        grad_text = [self.create_text("", "template", None, "explanation")]
        if self.grad_ind == False and self.expected_grad_date != "":
            if self.tense == 'future':
                grad_text = [
                    self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                    self.create_text(" has not graduated yet and the last semester ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" is eligible to apply for financial aid is ", "template", None, "explanation"),
                    self.create_text(self.expected_grad_date,"dynamic", "expected_grad_date", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]

            else:
                grad_text = [
                    self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                    self.create_text(" has not graduated yet while ", "template", None, "explanation"),
                    self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                    self.create_text(" was expected to graduate in ", "template", None, "explanation"),
                    self.create_text(self.expected_grad_date,"dynamic", "expected_grad_date", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]

            if str(self.recent_gpa) != 'nan' and self.recent_gpa != 0:
                grad_text += [
                    self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" latest cumulative GPA is ", "template", None, "explanation"),
                    self.create_text(str(self.recent_gpa),"dynamic", "CGPA", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]

        elif self.grad_ind == False and self.expected_grad_date == "":
            grad_text = [
                self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                self.create_text(" has not graduated yet and there is no information about ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" expected graduation date. ", "template", None, "explanation"),
            ]
            if str(self.recent_gpa) != 'nan' and self.recent_gpa != 0:
                grad_text += [
                    self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" latest cumulative GPA is ", "template", None, "explanation"),
                    self.create_text(str(self.recent_gpa),"dynamic", "CGPA", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
        elif self.grad_ind:
            grad_text = [
                self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                self.create_text(" graduated in ", "template", None, "explanation"),
                self.create_text(self.graduation_date,"dynamic", "graduation_date", "explanation"),
                self.create_text(" with a GPA of ", "template", None, "explanation"),
                self.create_text(str(self.graduation_gpa),"dynamic", "graduation_gpa", "explanation"),
                self.create_text(". ", "template", None, "explanation"),
            ]
        else:
            grad_text = [
                self.create_text(" There is no information about ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "semester_count", "explanation"),
                self.create_text(" graduation status nor graduation date. ", "template", None, "explanation"),
            ]
            if str(self.recent_gpa) != 'nan' and self.recent_gpa != 0:
                grad_text += [
                    self.create_text(self.pronoun_2.title(),"dynamic", "gender", "explanation"),
                    self.create_text(" latest cumulative GPA is ", "template", None, "explanation"),
                    self.create_text(str(self.recent_gpa),"dynamic", "CGPA", "explanation"),
                    self.create_text(". ", "template", None, "explanation"),
                ]
        return grad_text

    def get_credits_text(self):
        credits_text = [self.create_text("", "template", None, "explanation")]

        if self.passed_credits_count == 0:
            credits_text = [
                self.create_text("During ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" study in UNC Charlotte, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                self.create_text(" has attempted a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.attempted_credits_count),"dynamic", "attempted_credits", "explanation"),
                self.create_text(" credit hours and has not passed in any credit hours. ", "template", None, "explanation"),
            ]
        elif self.failed_credits_count == 0 and self.withdrawn_credits_count > 0:
            credits_text = [
                self.create_text("During ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" study in UNC Charlotte, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                self.create_text(" has attempted a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.attempted_credits_count),"dynamic", "attempted_credits", "explanation"),
                self.create_text(" credit hours, ", "template", None, "explanation"),
                self.create_text(self.pronoun.lower(),"dynamic", "gender", "explanation"),
                self.create_text(" has passed in a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.passed_credits_count),"dynamic", "credits_passed", "explanation"),
                self.create_text(" credit hours and has not failed in any credit hours. ", "template", None, "explanation"),
                self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                self.create_text(" has withdrawn a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.withdrawn_credits_count),"dynamic", "withdrawn_credits", "explanation"),
                self.create_text(" credit hours. ", "template", None, "explanation"),
            ]
        elif self.failed_credits_count > 0 and self.withdrawn_credits_count == 0:
            credits_text = [
                self.create_text("During ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" study in UNC Charlotte, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                self.create_text(" has attempted a total of ","template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.attempted_credits_count),"dynamic", "attempted_credits", "explanation"),
                self.create_text(" credit hours, ", "template", None, "explanation"),
                self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                self.create_text(" passed in a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.passed_credits_count),"dynamic", "credits_passed", "explanation"),
                self.create_text(" credit hours and failed in total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.failed_credits_count),"dynamic", "credits_failed", "explanation"),
                self.create_text(" credit hours. ", "template", None, "explanation"),
                self.create_text(self.pronoun.title(),"dynamic", "gender", "explanation"),
                self.create_text(" has not withdrawn any credit hours. ", "template", None, "explanation"),
            ]
        elif self.failed_credits_count == 0 and self.withdrawn_credits_count == 0:
            credits_text = [
                self.create_text("During ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" study in UNC Charlotte, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                self.create_text(" has attempted a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.attempted_credits_count),"dynamic", "attempted_credits", "explanation"),
                self.create_text(" credit hours and has passed in all of them. ", "template", None, "explanation"),
            ]
        elif self.passed_credits_count == self.attempted_credits_count:
            credits_text = [
                self.create_text("During ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" study in UNC Charlotte, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                self.create_text(" has attempted a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.attempted_credits_count),"dynamic", "attempted_credits", "explanation"),
                self.create_text(" credit hours and has passed in all of them. ", "template", None, "explanation"),
            ]
        else:
            credits_text = [
                self.create_text("During ", "template", None, "explanation"),
                self.create_text(self.pronoun_2,"dynamic", "gender", "explanation"),
                self.create_text(" study in UNC Charlotte, ", "template", None, "explanation"),
                self.create_text(self.first_name,"dynamic", "gender", "explanation"),
                self.create_text(" has attempted a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.attempted_credits_count),"dynamic", "attempted_credits", "explanation"),
                self.create_text(" credit hours. ", "template", None, "explanation"),
                self.create_text(self.pronoun,"dynamic", "gender", "explanation"),
                self.create_text(" has passed in a total of ", "template", None, "explanation"),
                self.create_text(self.p.number_to_words(self.passed_credits_count),"dynamic", "credits_passed", "explanation"),
                self.create_text(" credit hours. ", "template", None, "explanation"),
            ]
        return credits_text