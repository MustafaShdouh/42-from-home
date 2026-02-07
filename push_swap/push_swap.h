/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 17:58:46 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/06 21:10:01 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <unistd.h>
# include <stdlib.h>
# include <limits.h>

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
// stacks:
int		stack_size(t_stack *stack);
t_stack	*stack_new(int value);
t_stack *stack_last(t_stack *stack);
void	stack_add_back(t_stack **stack, t_stack *new);
void free_stack(t_stack **stack);
int	is_sorted(t_stack *stack);
int find_min(t_stack *stack);
int find_max(t_stack *stack);

//operations:
static void push_stack(t_stack **a, t_stack **b);
void pa(t_stack **a, t_stack **b);
void pb(t_stack **a, t_stack **b);
static void swap_stack(t_stack **s);
void	sa(t_stack **a);
void	sb(t_stack **b);
void	ss(t_stack **a, t_stack **b);
static void rotate_stack(t_stack **s);
void	ra(t_stack **a);
void	rb(t_stack **b);
void	rr(t_stack **a, t_stack **b);
static void rev_rotate_stack(t_stack **s);
void	rra(t_stack **a);
void	rrb(t_stack **b);
void	rrr(t_stack **a, t_stack **b);
//disorder:
double	compute_disorder(t_stack *a);
// strategies:
void	sort_simple(t_stack **a, t_stack **b, int *count);
void	sort_complex(t_stack **a, t_stack **b, int *count);
void	index_stack(t_stack *stack);

#endif