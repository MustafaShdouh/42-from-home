/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/04 17:58:46 by mel-shdo          #+#    #+#             */
/*   Updated: 2026/02/04 22:16:14 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

#include <unistd.h>
#include <stdlib.h>
#include <limits.h>

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
} t_strategy

#endif