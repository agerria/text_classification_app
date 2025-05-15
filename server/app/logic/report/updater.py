from .cmp_methods import (
    CmpResult,
    paired_t_test,
    wilcoxon_signed_rank_test,
    bootstrap_mean_difference,
    mcnemar_test,
)

class ReportUpdater:
    def __init__(self, report):
        self.report = report
        # self.fields_to_process = ['fold-wa-f1-stratified', 'fold-wa-f1-random']
        self.fields_to_process = {
            'fold-wa-f1-ttest-stratified': paired_t_test,
            'fold-wa-f1-ttest-random': paired_t_test,
            'fold-wa-f1-wilcoxon-stratified': wilcoxon_signed_rank_test,
            'fold-wa-f1-wilcoxon-random': wilcoxon_signed_rank_test,
            'fold-wa-f1-bootstrap-stratified': bootstrap_mean_difference,
            'fold-wa-f1-bootstrap-random': bootstrap_mean_difference,
            
            'fold-wa-rc-ttest-stratified': paired_t_test,
            'fold-wa-rc-ttest-random': paired_t_test,
            'fold-wa-rc-wilcoxon-stratified': wilcoxon_signed_rank_test,
            'fold-wa-rc-wilcoxon-random': wilcoxon_signed_rank_test,
            'fold-wa-rc-bootstrap-stratified': bootstrap_mean_difference,
            'fold-wa-rc-bootstrap-random': bootstrap_mean_difference,
            
            'fold-wa-pr-ttest-stratified': paired_t_test,
            'fold-wa-pr-ttest-random': paired_t_test,
            'fold-wa-pr-wilcoxon-stratified': wilcoxon_signed_rank_test,
            'fold-wa-pr-wilcoxon-random': wilcoxon_signed_rank_test,
            'fold-wa-pr-bootstrap-stratified': bootstrap_mean_difference,
            'fold-wa-pr-bootstrap-random': bootstrap_mean_difference,
            
            
            'fold-ma-f1-ttest-stratified': paired_t_test,
            'fold-ma-f1-ttest-random': paired_t_test,
            'fold-ma-f1-wilcoxon-stratified': wilcoxon_signed_rank_test,
            'fold-ma-f1-wilcoxon-random': wilcoxon_signed_rank_test,
            'fold-ma-f1-bootstrap-stratified': bootstrap_mean_difference,
            'fold-ma-f1-bootstrap-random': bootstrap_mean_difference,

            'fold-ma-rc-ttest-stratified': paired_t_test,
            'fold-ma-rc-ttest-random': paired_t_test,
            'fold-ma-rc-wilcoxon-stratified': wilcoxon_signed_rank_test,
            'fold-ma-rc-wilcoxon-random': wilcoxon_signed_rank_test,
            'fold-ma-rc-bootstrap-stratified': bootstrap_mean_difference,
            'fold-ma-rc-bootstrap-random': bootstrap_mean_difference,

            'fold-ma-pr-ttest-stratified': paired_t_test,
            'fold-ma-pr-ttest-random': paired_t_test,
            'fold-ma-pr-wilcoxon-stratified': wilcoxon_signed_rank_test,
            'fold-ma-pr-wilcoxon-random': wilcoxon_signed_rank_test,
            'fold-ma-pr-bootstrap-stratified': bootstrap_mean_difference,
            'fold-ma-pr-bootstrap-random': bootstrap_mean_difference,
            
            
            'predicts-stratified': mcnemar_test,
            'predicts-random': mcnemar_test,
        }


    def update_report(self):
        self.updated = {}
        for field in self.fields_to_process.keys():
            self.process_field(field)
            self.update_indicators(field)
        return self.report


    def process_field(self, field):
        self.updated[field] = {}
        for column in self.report:
            hash = column['hash']
            indicators = column.get('indicators', {})
            current_folds = indicators.get(field)

            cmps = {}
            for other_column in self.report:
                other_hash = other_column['hash']
                if other_hash == hash:
                    continue
                other_indicators = other_column.get('indicators', {})
                other_folds = other_indicators.get(field)

                comparison_result = self.compare_folds(field, current_folds, other_folds)
                cmps[other_hash] = comparison_result

            new_fold_obj = {
                'folds': current_folds,
                'cmps': cmps,
                'hash': hash,
            }
            self.updated[field][hash] = new_fold_obj


    def compare_folds(self, field, folds1, folds2) -> CmpResult:
        if self.are_folds_valid(folds1) and self.are_folds_valid(folds2):
            return self.fields_to_process[field](folds1, folds2)
            # return self.compare_function(folds1, folds2)
        
        return CmpResult(is_valid=False)
        return None


    def update_indicators(self, field):
        for column in self.report:
            hash = column['hash']
            indicators = column.get('indicators', {})
            indicators[field] = self.updated[field][hash]
        

    @staticmethod
    def are_folds_valid(folds):
        if folds is None:
            return False
        
        if isinstance(folds, dict) and folds != {}:
            return True
        
        if not isinstance(folds, list) or len(folds) == 0:
            return False
        for item in folds:
            if not isinstance(item, (int, float)):
                return False
        return True

    @staticmethod
    def compare_function(arr1, arr2):
        return sum(arr1) - sum(arr2)
