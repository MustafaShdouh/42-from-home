/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 17:58:46 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/14 01:08:53 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>
# include <limits.h>

typedef struct s_op_stats
{
	int	sa;
	int	sb;
	int	ss;
	int	pa;
	int	pb;
	int	ra;
	int	rb;
	int	rr;
	int	rra;
	int	rrb;
	int	rrr;
	int	print_ops;
}	t_op_stats;

typedef struct stack_to_sort
{
	int						content;
	int						index;
	struct stack_to_sort	*next;
	struct stack_to_sort	*prev;
}	t_stack;

typedef enum e_strategy
{
	START_ADAPTIVE,
	START_SIMPLE,
	START_MEDIUM,
	START_COMPLEX
}	t_strategy;

t_op_stats	*get_stats(void);
t_stack		*stack_new(int value);
t_stack		*stack_last(t_stack *stack);
void		stack_add_back(t_stack **stack, t_stack *new);
void		free_stack(t_stack **stack);
int			is_sorted(t_stack *stack);
int			find_min(t_stack *stack);
int			find_max(t_stack *stack);
int			stack_size(t_stack *stack);
void		pa(t_stack **a, t_stack **b);
void		pb(t_stack **a, t_stack **b);
void		sa(t_stack **a);
void		sb(t_stack **b);
void		ss(t_stack **a, t_stack **b);
void		ra(t_stack **a);
void		rb(t_stack **b);
void		rr(t_stack **a, t_stack **b);
void		rra(t_stack **a);
void		rrb(t_stack **b);
void		rrr(t_stack **a, t_stack **b);
double		compute_disorder(t_stack *a);
void		sort_simple(t_stack **a, t_stack **b);
void		sort_medium(t_stack **a, t_stack **b);
void		sort_complex(t_stack **a, t_stack **b);
void		sort_adaptive(t_stack **a, t_stack **b);
void		sort_three(t_stack **a);
void		index_stack(t_stack *stack);
void		print_bench(t_strategy mode, double disorder);
void		ft_putfloat_fd(double num, int fd);
long		ft_atol(const char *str);
int			ft_strcmp(const char *s1, const char *s2);
void		parse_args(int argc, char **argv, t_stack **stack_a);
char		**ft_split_whitespace(char *str);
int			error_syntax(char *str_n);
int			error_duplicate(t_stack *a, int n);
void		ft_error(t_stack **a, t_stack **b);

#endif